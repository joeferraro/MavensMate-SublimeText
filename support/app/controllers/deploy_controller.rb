# encoding: utf-8
require ENV['TM_BUNDLE_SUPPORT'] + '/lib/mavensmate.rb'
require ENV['TM_BUNDLE_SUPPORT'] + '/lib/factory.rb'
require ENV['TM_BUNDLE_SUPPORT'] + '/lib/metadata_helper.rb'
require ENV['TM_BUNDLE_SUPPORT'] + '/lib/object.rb'
require ENV['TM_BUNDLE_SUPPORT'] + '/lib/util.rb'
class DeployController < ApplicationController
  
  include MetadataHelper  
  
  layout "base", :only => [:index, :index_new, :show_compile_result] 
          
  def index
    if File.not.exist? "#{ENV['TM_PROJECT_DIRECTORY']}/config/.org_metadata"
      MavensMate.build_index
    else     
      confirmed = TextMate::UI.request_confirmation(
        :title => "MavensMate",
        :prompt => "Would you like to refresh the local index of your Salesforce.com org's metadata?",
        :button1 => "Refresh",
        :button2 => "No")
    end
    
    connections = []
    begin
      pconfig = MavensMate.get_project_config
      pconfig['org_connections'].each do |connection| 
        pw = KeyChain::find_internet_password("#{pconfig['project_name']}-mm-#{connection['username']}")
        server_url = connection["environment"] == "production" ? "https://www.salesforce.com" : "https://test.salesforce.com" 
        connections.push({
          :un => connection["username"], 
          :pw => pw,
          :server_url => server_url
        })
      end 
    rescue Exception => e
      #no connections
    end
    
    changesets = []
    if File.directory?("#{ENV['TM_PROJECT_DIRECTORY']}/changesets")
      Dir.foreach("#{ENV['TM_PROJECT_DIRECTORY']}/changesets") do |c|
        next if c == "." or c == ".."
        changesets.push(c)
      end                                                            
    end
    
    MavensMate.build_index if confirmed
    meta_array = eval(File.read("#{ENV['TM_PROJECT_DIRECTORY']}/config/.org_metadata")) #=> comprehensive list of server metadata    
    render "_deploy", :locals => { :meta_array => meta_array, :child_metadata_definition => CHILD_META_DICTIONARY, :connections => connections, :changesets => changesets }
  end
  
  def index_new
    # if File.not.exist? "#{ENV['TM_PROJECT_DIRECTORY']}/config/.org_metadata"
    #   MavensMate.build_index
    # else     
    #   confirmed = TextMate::UI.request_confirmation(
    #     :title => "MavensMate",
    #     :prompt => "Would you like to refresh the local index of your Salesforce.com org's metadata?",
    #     :button1 => "Refresh",
    #     :button2 => "No")
    # end    
    
    confirmed = false
    
    connections = []
    begin
      pconfig = MavensMate.get_project_config
      pconfig['org_connections'].each do |connection| 
        pw = KeyChain::find_internet_password("#{pconfig['project_name']}-mm-#{connection['username']}")
        server_url = connection["environment"] == "production" ? "https://www.salesforce.com" : "https://test.salesforce.com" 
        connections.push({
          :un => connection["username"], 
          :pw => pw,
          :server_url => server_url
        })
      end 
    rescue Exception => e
      #no connections
    end
    
    changesets = []
    if File.directory?("#{ENV['TM_PROJECT_DIRECTORY']}/changesets")
      Dir.foreach("#{ENV['TM_PROJECT_DIRECTORY']}/changesets") do |c|
        next if c == "." or c == ".."
        changesets.push(c)
      end                                                            
    end
    
    MavensMate.build_index if confirmed
    meta_array = eval(File.read("#{ENV['TM_PROJECT_DIRECTORY']}/config/.org_metadata")) #=> comprehensive list of server metadata    
    render "_deploy_compare", :locals => { :meta_array => meta_array, :child_metadata_definition => CHILD_META_DICTIONARY, :connections => connections, :changesets => changesets }
  end
  
  def diff
    tree = eval(params[:tree])      
    params[:package] = tree
    result = MavensMate.diff(params)
    render "_diff_result", :locals => { :result => result, :orgs => params[:orgs] }
  end
  
  #deploys metadata to selected server
  def deploy_metadata      
    if params[:mode] == "async"      
      exit if fork            # Parent exits, child continues.
      Process.setsid          # Become session leader.
      exit if fork            # Zap session leader.   
      pid = fork do
        begin
          tree = eval(params[:tree])      
          params[:package] = tree
          destination = params[:un]
          is_check_only = params[:check_only]          
          result = MavensMate.deploy_to_server(params)
          result = MavensMate::Util.parse_deploy_response(result)
          `osascript '#{ENV['TM_BUNDLE_SUPPORT']}/osx/growl.scpt' 'Deploy complete'`
                    
          require 'erb'
          template = ERB.new File.new("#{ENV['TM_BUNDLE_SUPPORT']}/app/views/deploy/_async_deploy_result.html.erb").read, nil, "-"
          erb = template.result(binding)        
          src = File.new("#{ENV['TM_PROJECT_DIRECTORY']}/config/.async_deploy_result.html", "w")
          src.puts(erb)
          src.close
          MavensMate.close_deploy_window          
          `open "#{ENV['TM_PROJECT_DIRECTORY']}/config/.async_deploy_result.html"`        
        rescue Exception => e
          TextMate::UI.alert(:warning, "MavensMate", e.message + "\n" + e.backtrace.join("\n"))  
        end  
      end
      Process.detach(pid)
    else
      begin
        tree = eval(params[:tree])      
        params[:package] = tree
        result = MavensMate.deploy_to_server(params)
        result = MavensMate::Util.parse_deploy_response(result)
        render "_deploy_result", :locals => { :result => result, :is_check_only => params[:check_only] }
        `osascript '#{ENV['TM_BUNDLE_SUPPORT']}/osx/growl.scpt' 'Deploy complete'`
      rescue Exception => e
        TextMate::UI.alert(:warning, "MavensMate", e.message + "\n" + e.backtrace.join("\n"))  
      end
    end
  end
  
  #special method only used for displaying the result of a compile file/project command via exit_show_html
  def show_compile_result  
    begin
      result = MavensMate::Util.parse_deploy_response(params[:result])
      begin
        message = result[:messages][0]
        file_name = message[:file_name]
				fns = message[:file_name].split("/")
				file_name = fns[fns.length - 1]   			         	
				full_path =  "#{ENV['TM_PROJECT_DIRECTORY']}/src/#{message[:file_name]}"
				full_path.gsub!(/unpackaged\//, '')
        TextMate.go_to(:file => full_path, :line => message[:line_number], :column => message[:column_number])        
      rescue
        #TODO: for now we're ok with this
      end
      render "_compile_result", :locals => { :result => result, :is_check_only => false }
    rescue Exception => e
      TextMate::UI.alert(:warning, "MavensMate", e.message + "\n" + e.backtrace.join("\n"))  
    end
  end
  
end