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
    my_json = File.read("#{ENV['TM_BUNDLE_SUPPORT']}/conf/metadata_describe.json")
    support_folder = ENV['TM_BUNDLE_SUPPORT']
    sf = support_folder.gsub(/lib\/../, "")
    render "_project_new", :locals => { :user_action => params[:user_action], :my_json => my_json, :child_metadata_definition => CHILD_META_DICTIONARY, :support_folder => sf}
  end 
   
  def index_edit
    pconfig = MavensMate.get_project_config
    password = KeyChain::find_internet_password("#{pconfig['project_name']}-mm")
    render "_project_edit", :locals => { :child_metadata_definition => CHILD_META_DICTIONARY, :pname => pconfig['project_name'], :pun => pconfig['username'], :ppw => password, :pserver => pconfig['environment'] }
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