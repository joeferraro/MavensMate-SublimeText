# encoding: utf-8
require SUPPORT + '/lib/mavensmate.rb'
require SUPPORT + '/lib/factory.rb' 
require SUPPORT + '/lib/keychain.rb' 
require SUPPORT + '/lib/lsof.rb'
require SUPPORT + '/lib/object.rb'
require 'json'

class ProjectController < ApplicationController
  
  include MetadataHelper
  
  attr_accessor :client
  
  layout "base", :only => [:index_new, :index_edit, :index_new_changeset]

  def index_new
    kill_server
    my_json = File.read("#{ENV['TM_BUNDLE_SUPPORT']}/conf/metadata_describe.json")
    support_folder = ENV['TM_BUNDLE_SUPPORT']
    sf = support_folder.gsub(/lib\/../, "")
    render "_project_new", :locals => { :user_action => params[:user_action], :my_json => my_json, :child_metadata_definition => CHILD_META_DICTIONARY, :support_folder => sf}
  end 
   
  def index_edit    
    kill_server
    if File.not.exist? "#{ENV['TM_PROJECT_DIRECTORY']}/config/.org_metadata"
      MavensMate.build_index
    else     
      confirmed = TextMate::UI.request_confirmation(
        :title => "MavensMate",
        :prompt => "Would you like to refresh the local index of your Salesforce.com org's metadata?",
        :button1 => "Refresh",
        :button2 => "No")
    end  
    
    MavensMate.build_index if confirmed
    
    project_array = eval(File.read("#{ENV['TM_PROJECT_DIRECTORY']}/config/.org_metadata")) #=> comprehensive list of server metadata
    
    require 'rubygems'
    require 'nokogiri'
    project_package = Nokogiri::XML(File.open("#{ENV['TM_PROJECT_DIRECTORY']}/src/package.xml"))
    project_package.remove_namespaces!
    project_package.xpath("//types/name").each do |node|
      object_definition = MavensMate::FileFactory.get_meta_type_by_name(node.text) || MavensMate::FileFactory.get_child_meta_type_by_name(node.text)  
      #=> ApexClass
      is_parent = !object_definition[:parent_xml_name]
      server_object = project_array.detect { |f| f[:key] == node.text }
      next if server_object.nil? && is_parent
            
      if is_parent
        server_object[:selected] = "selected"
        server_object[:select_mode] = (node.previous_element.text == "*") ? "all" : "some"
        MavensMate.select_all(server_object) if server_object[:select_mode] == "all"
        next if server_object[:selected] == "all"     
      end
      
      if not is_parent
        #=> CustomField
        parent_object_definition = MavensMate::FileFactory.get_meta_type_by_name(object_definition[:parent_xml_name]) #=> CustomObject
        prev_node = node.previous_element    
        while prev_node.not.nil? && prev_node.node_name == "members"
          next if prev_node.text.not.include? "."
          obj_name = prev_node.text.split(".")[0] #=> Lead
          obj_attribute = prev_node.text.split(".")[1] #=> Field_Name__c
           
          server_object = project_array.detect { |f| f[:key] == object_definition[:parent_xml_name] } #=> CustomObject
          sobject = server_object[:children].detect {|f| f[:title] == obj_name } #=> Lead
          sobject_metadata = sobject[:children].detect {|f| f[:title] == object_definition[:tag_name] } #=> fields
          sobject_metadata[:children].each do |item|
            if item[:title] == obj_attribute
              item[:selected] = "selected"
              break
            end
          end          
          prev_node = prev_node.previous_element || nil
        end
      end
      
      prev_node = node.previous_element    
      while prev_node.not.nil? && prev_node.node_name == "members"
        #skip items in folders for now
        if prev_node.include? "/"
          prev_node = prev_node.previous_element || nil
          next
        end
        child_object = server_object[:children].detect {|f| f[:key] == prev_node.text }
        child_object[:selected] = "selected" if child_object.not.nil?
        MavensMate.select_all(child_object) if object_definition[:child_xml_names]
        prev_node = prev_node.previous_element || nil
      end
      
      prev_node = node.previous_element    
      while prev_node.not.nil? && prev_node.node_name == "members"
        #process only items in folders
        if prev_node.text.not.include? "/"
          prev_node = prev_node.previous_element || nil
          next
        end
        child_object = server_object[:children].detect {|f| f[:key] == prev_node.text.split("/")[0]}        
        begin  
          child_object[:children].each do |gchild|
            gchild[:selected] = "selected" if gchild[:key] == prev_node.text
          end
        rescue Exception => e
          #puts e.message + "\n" + e.backtrace.join("\n")
        end
        prev_node = prev_node.previous_element || nil
      end
    end
    
    pconfig = MavensMate.get_project_config
    password = KeyChain::find_internet_password("#{pconfig['project_name']}-mm")
    
    render "_project_edit", :locals => { :package => project_package, :project_array => project_array, :child_metadata_definition => CHILD_META_DICTIONARY, :pname => pconfig['project_name'], :pun => pconfig['username'], :ppw => password, :pserver => pconfig['environment'] }
  end
    
  #updates current project
  def update
    begin     
      tree = eval(params[:tree])  
      result = MavensMate.clean_project({ :update_sobjects => false, :update_package => true, :package => tree })
      render "_project_edit_result", :locals => { :message => result[:message], :success => result[:success] }
    rescue Exception => e
      TextMate::UI.alert(:warning, "MavensMate", e.message + "\n" + e.backtrace.join("\n"))
    end
  end
  
  #update project creds
  def update_creds
    begin
      un = params[:un]
      pw = params[:pw]
      server_url = params[:server_url]

      TextMate.call_with_progress( :title => "MavensMate", :message => "Validating Salesforce.com Credentials" ) do
        client = MavensMate::Client.new({ :username => params[:un], :password => params[:pw], :endpoint => params[:server_url] })
      end
      
      TextMate.call_with_progress( :title => "MavensMate", :message => "Updating project configuration" ) do
        environment = (server_url.include? "test") ? "sandbox" : "production"
        require 'yaml'
        yml = YAML::load(File.open("#{ENV['TM_PROJECT_DIRECTORY']}/config/settings.yaml")) 
        project_name = yml['project_name']
        yml['username'] = un
        yml['environment'] = environment 
        File.open("#{ENV['TM_PROJECT_DIRECTORY']}/config/settings.yaml", 'w') { |f| YAML.dump(yml, f) }
        MavensMate.add_to_keychain(project_name, pw) 
      end 
    rescue Exception => e
      TextMate::UI.alert(:warning, "MavensMate", e.message)
    end
  end
  
  #checks provided salesforce.com credentials    
  def login
    if params[:un].nil? || params[:pw].nil? || params[:server_url].nil?
      TextMate::UI.alert(:warning, "MavensMate", "Please provide Salesforce.com credentials before selecting metadata")
      abort
    end
      
    begin
      TextMate.call_with_progress( :title => "MavensMate", :message => "Validating Salesforce.com Credentials" ) do
        self.client = MavensMate::Client.new({ :username => params[:un], :password => params[:pw], :endpoint => params[:server_url] })
      end
      #$stdout.flush
      #flush
      if ! self.client.sid.nil? && ! self.client.metadata_server_url.nil?
        puts "<input type='hidden' value='#{self.client.sid}' id='sid'/>"
        puts "<input type='hidden' value='#{self.client.metadata_server_url}' id='murl'/>"
      end
    rescue Exception => e
      TextMate::UI.alert(:warning, "MavensMate", e.message)
      return
    end
  end
  
  #creates new local project from selected salesforce data
  def new_custom_project  
    begin
      tree = eval(params[:tree])
      params[:package] = tree
      result = MavensMate.new_project(params)
      return if result.nil?
      kill_server unless ! result[:is_success] 
      MavensMate.close_all_html_windows unless ! result[:is_success]
      render "_project_new_result", :locals => { :message => result[:error_message], :success => result[:is_success] }
    rescue Exception => e
      TextMate::UI.alert(:warning, "MavensMate", e.message)
    end
  end
      
  #checks out project from SVN, associates Salesforce.com server credentials  
  def checkout
    begin
      result = MavensMate.checkout_project(params)
      return if result.nil?
      kill_server unless ! result[:is_success]
      MavensMate.close_all_html_windows unless ! result[:is_success]    
      render "_project_new_result", :locals => { :message => result[:error_message], :success => result[:is_success] } 
    rescue Exception => e
      TextMate::UI.alert(:warning, "MavensMate", e.message)
    end
  end
  
  def start_tcp_server
    exit if fork            # Parent exits, child continues.
    Process.setsid          # Become session leader.
    exit if fork            # Zap session leader.
    
    require 'socket'
    require 'uri'
    pid = fork do
      webserver = TCPServer.new('127.0.0.1', 7125)
      while (session = webserver.accept)
         begin 
           session.print "HTTP/1.1 200/OK\r\nContent-type:application/json\r\n\r\n"
           request = session.gets
           request.gsub!(/GET\ \//, '').gsub!(/\ HTTP.*/, '')
           request_params = request[request.index("?")+1,request.length-1]
           response = []
           if request_params.include? "vc_type" and request_params.include? "vc_url" and request_params.include? "svn_un" and request_params.include? "svn_pw"
             response = handle_vc_request(request_params)
             session.puts response.to_json 
           else
             response = handle_metadata_request(request_params)
             session.puts response
           end
         rescue Exception => e
           session.puts e.message + "\n" + e.backtrace.join("\n")
         end
         session.close
      end
    end   
    Process.detach(pid)
    puts "<input type='hidden' value='#{pid}' id='pid'/>"    
  end
  
  def handle_vc_request(request_params)
    svn_un, svn_pw, vc_type, vc_url = nil, nil, nil, nil
    param_array = request_params.split("&")
    param_array.each do |param|
      p = param.split("=")
      if p[0] == "vc_url"
        vc_url = URI.unescape(p[1])
        vc_url.gsub!(" ", "/\ ") 
        vc_url.chomp!
        vc_url.chop! if vc_url[vc_url.length-1,1] == "/"
      elsif p[0] == "vc_type"
        vc_type = p[1].downcase!
      elsif p[0] == "svn_un"
        svn_un = p[1]
        svn_un.chomp! if svn_un.not.nil?
      elsif p[0] == "svn_pw"
        svn_pw = p[1]
        svn_pw.chomp! if svn_pw.not.nil?
      end  
    end
    
    require 'rubygems'
    require 'nokogiri'
    opts = []
    if vc_type == "svn"
      response = %x{svn list --xml --username #{svn_un} --password #{svn_pw} '#{vc_url}'}                    
      doc = Nokogiri::XML(response)
      doc.remove_namespaces!
      doc.xpath("//entry/name").each do |node|
        opts.push({:url => vc_url+"/"+node.text, :title => node.text})
      end 
    elsif vc_type == "git"
      response = %x{git ls-remote '#{vc_url}'} 
      response.split("\n").each do |branch|
        branch_name = branch.split("\t")[1]
        opts.push({ :url => branch_name, :title => branch_name })
      end 
    end
    return opts
  end
  
  def handle_metadata_request(request_params)
    param_array = request_params.split("&")
    sid, metadata_server_url, meta_type = "", "", ""
    param_array.each { |param|
      pair = param.split("=")
      if pair[0] == "sid"
        sid = pair[1]
      elsif pair[0] == "murl"
        metadata_server_url = pair[1]
      elsif pair[0] == "key"
        meta_type = pair[1]
      end 
    }
    metadata_server_url = URI.unescape(metadata_server_url)
    client = MavensMate::Client.new({ :sid => sid, :metadata_server_url => metadata_server_url })
    return client.list(meta_type, false)     
  end
        
  private
    
    #stops TCP server proc
    def kill_server
      if Lsof.running?(7125)
        Lsof.kill(7125)
      end
    end
    
end