# encoding: utf-8
require SUPPORT + '/lib/mavensmate.rb'
require SUPPORT + '/lib/factory.rb'
require SUPPORT + '/lib/metadata_helper.rb'
require SUPPORT + '/lib/object.rb'
require SUPPORT + '/lib/util.rb'
class DeployController < ApplicationController
  
  include MetadataHelper  
  
  layout "base", :only => [:index, :index_new, :show_compile_result] 
          
  def index
    connections = []
    begin
      pconfig = MavensMate.get_project_config
      pconfig['org_connections'].each do |connection| 
        pw = KeyChain::find_internet_password("#{pconfig['project_name']}-mm-#{connection['username']}")
        server_url = connection["environment"] == "production" ? "https://www.salesforce.com" : "https://test.salesforce.com" 
        #server_url = MavensMate::Util.get_sfdc_endpoint_by_type(connection["environment"])  
        connections.push({
          :un => connection["username"], 
          :pw => pw,
          :server_url => server_url,
          :type => connection["environment"]
        })
      end 
    rescue Exception => e
      #no connections
    end
    
    changesets = []
    # if File.directory?("#{ENV['MM_CURRENT_PROJECT_DIRECTORY']}/changesets")
    #   Dir.foreach("#{ENV['MM_CURRENT_PROJECT_DIRECTORY']}/changesets") do |c|
    #     next if c == "." or c == ".."
    #     changesets.push(c)
    #   end                                                            
    # end
    
    #MavensMate.build_index if confirmed
    #meta_array = eval(File.read("#{ENV['MM_CURRENT_PROJECT_DIRECTORY']}/config/.org_metadata")) #=> comprehensive list of server metadata    
    render "_deploy", :locals => { :child_metadata_definition => CHILD_META_DICTIONARY, :connections => connections, :changesets => changesets }
  end
  
  def index_new
    # if File.not.exist? "#{ENV['MM_CURRENT_PROJECT_DIRECTORY']}/config/.org_metadata"
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
    if File.directory?("#{ENV['MM_CURRENT_PROJECT_DIRECTORY']}/changesets")
      Dir.foreach("#{ENV['MM_CURRENT_PROJECT_DIRECTORY']}/changesets") do |c|
        next if c == "." or c == ".."
        changesets.push(c)
      end                                                            
    end
    
    MavensMate.build_index if confirmed
    meta_array = eval(File.read("#{ENV['MM_CURRENT_PROJECT_DIRECTORY']}/config/.org_metadata")) #=> comprehensive list of server metadata    
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
          `osascript '#{SUPPORT}/osx/growl.scpt' 'Deploy complete'`
                    
          require 'erb'
          template = ERB.new File.new("#{SUPPORT}/app/views/deploy/_async_deploy_result.html.erb").read, nil, "-"
          erb = template.result(binding)        
          src = File.new("#{ENV['MM_CURRENT_PROJECT_DIRECTORY']}/config/.async_deploy_result.html", "w")
          src.puts(erb)
          src.close
          MavensMate.close_deploy_window          
          `open "#{ENV['MM_CURRENT_PROJECT_DIRECTORY']}/config/.async_deploy_result.html"`        
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
        `osascript '#{SUPPORT}/osx/growl.scpt' 'Deploy complete'`
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
				full_path =  "#{ENV['MM_CURRENT_PROJECT_DIRECTORY']}/src/#{message[:file_name]}"
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