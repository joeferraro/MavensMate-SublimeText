# encoding: utf-8
require 'rubygems'
require 'fileutils'
require 'yaml'   
require ENV['TM_BUNDLE_SUPPORT'] + '/lib/mavensmate.rb'

class EventServerController < ApplicationController
  include MetadataHelper

  layout "base", :only => [:index]
             
  def index
    running = false
    pid = ""
    if File.exist? "#{ENV['TM_PROJECT_DIRECTORY']}/config/.event_server"
      yml = YAML::load(File.open("#{ENV['TM_PROJECT_DIRECTORY']}/config/.event_server"))
      pid = yml["pid"]
      running = true if pid != nil
    end   
    render "_index", :locals => { :running => running, :pid => pid }
  end
  
  #write process id to config file
  def write_server_status(pid)
    File.open("#{ENV['TM_PROJECT_DIRECTORY']}/config/.event_server", 'w') {|f| f.write("pid: #{pid}") }
  end
  
  #kills the server process (manually)
  def stop_server
    FileUtils.rm_r "#{ENV['TM_PROJECT_DIRECTORY']}/config/.event_server"
    pid = params[:pid]
    `kill #{pid}`
    render "_index", :locals => { :running => false, :pid => "" }  
  end 
  
  #kill server when tm process has been killed
  def self.kill_server(pd)
    require 'yaml'
    begin
      yml = YAML::load(File.open("#{pd}/config/.event_server"))
      pid = yml["pid"]
      FileUtils.rm_rf "#{pd}/config/.event_server"
      `kill #{pid}`
    rescue Exception => e
      if ! e.message.include? "SIGTERM"
        File.open("#{pd}/config/.event_server_exception", 'a') {|f| f.write(e.message + "\n" + e.backtrace.join("\n")) }
      end
    end
  end
  
  #start & daemonize notification server  
  def start_server
    exit if fork            # Parent exits, child continues.
    Process.setsid          # Become session leader.
    exit if fork            # Zap session leader.
    
    pid = fork do
      poll_frequency = ENV['FM_EVENT_POLL_FREQ'] || 1
      pd = ENV['TM_PROJECT_DIRECTORY']
      types = ["ApexClass", "ApexTrigger", "ApexPage", "ApexComponent"]
      # :startDate => '2012-01-13T13:18:31Z',
      # :endDate => '2012-02-01T13:18:31Z'  
      sd = DateTime.now - 1 #was 0
      ed = DateTime.now

      client = MavensMate::Client.new  
      
      begin
        loop do    
          types.each_with_index do |mt, i|
            body =  "<wsdl:sObjectTypeEntityType>#{mt}</wsdl:sObjectTypeEntityType>"
            body << "<ins0:startDate>#{sd.to_s}</ins0:startDate>"
            body << "<ins0:endDate>#{ed.to_s}</ins0:endDate>"

            response = client.pclient.request :get_updated do |soap|
                soap.header = {
                  "SessionHeader" => {
                    :session_id => client.sid
                  },
                  :attributes! => { "SessionHeader" => { "xmlns" => "urn:partner.soap.sforce.com" } } 
                }  
                soap.body = body
            end

            res = response.to_hash[:get_updated_response][:result]
            if res[:ids]
              ids = []
              if ! res[:ids].kind_of? Array
                ids.push(res[:ids])
              else
                ids = res[:ids]
              end
              EventServerController.notify(client, mt, ids)
            end

            last_date = res[:latest_date_covered]    
            sd = last_date.to_s if i == 0       
          end   
                  
          break if EventServerController.tm_is_running == "false"
          
          sleep poll_frequency.to_i * 60
          ed = DateTime.now.to_s 
        end
        EventServerController.kill_server(pd)
      rescue Exception => e
        if ! e.message.include? "SIGTERM"
          File.open("#{pd}/config/.event_server_exception", 'a') {|f| f.write(e.message + "\n" + e.backtrace.join("\n")) }
        end
      end   
    
    end   
    Process.detach(pid)
    write_server_status(pid) 
    render "_index", :locals => { :running => true, :pid => pid }
  end
  
  #determines whether TextMate.app is running #=> "true" or "false"
  def self.tm_is_running
    res = `osascript '#{ENV['TM_BUNDLE_SUPPORT']}/osx/isapprunning.scpt'`
    res.chomp!
    return res
  end
  
  #sends growl notifications for modified metadata
  def self.notify(client, sobject_name, ids)
    id_list = ids.map {|item| "Id = '#{item}'"}
    id_list = id_list.join(" OR ")
    response = client.pclient.request :query do |soap|
        soap.header = {
        "SessionHeader" => {
          :session_id => client.sid
        },
          :attributes! => { "SessionHeader" => { "xmlns" => "urn:partner.soap.sforce.com" } } 
        }  
        soap.body = { 
          :queryString => "Select Name, LastModifiedBy.Name From #{sobject_name} Where (#{id_list}) AND LastModifiedById != '#{client.user_id}'" 
        }
    end
    response_hash = response.to_hash
    puts response_hash.inspect
    qr = response_hash[:query_response][:result]
    records = []
    if ! qr[:records].kind_of? Array
      records.push(qr[:records])
    else
      records = qr[:records]
    end
    
    if records.size <= 5    
      records.each do |r|
        `osascript '#{ENV['TM_BUNDLE_SUPPORT']}/osx/growl.scpt' '#{r[:name]}#{META_EXT_MAP[r[:type]]} was modified by #{r[:last_modified_by][:name]}'`     
      end
    else
      `osascript '#{ENV['TM_BUNDLE_SUPPORT']}/osx/growl.scpt' '#{records.size.to_s} #{META_DIR_MAP[records[0][:type]]} were modified'`     
    end      
  end
end