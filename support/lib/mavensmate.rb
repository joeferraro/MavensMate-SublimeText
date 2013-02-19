require 'rubygems'
require 'rexml/document'
require 'fileutils'  
require 'json'
require SUPPORT + '/lib/client'
require SUPPORT + '/lib/factory'
require SUPPORT + '/lib/exceptions'
require SUPPORT + '/lib/metadata_helper'
require SUPPORT + '/lib/util'
require SUPPORT + '/lib/logger'

STDOUT.sync = true

module MavensMate
  
  include MetadataHelper
  
  def self.logger
    return MavensMate::Log.instance
  end

  def self.new_project_from_existing_directory(params)
    begin
      project_name        = params[:pn]
      un                  = params[:un]
      pw                  = params[:pw]
      server_url          = params[:server_url]
      existing_location   = params[:existing_location]
      endpoint            = MavensMate::Util.get_sfdc_endpoint(server_url)      

      client = MavensMate::Client.new({ :username => un, :password => pw, :endpoint => endpoint })
      Thread.abort_on_exception = true
      threads = []
      MavensMate::FileFactory.put_project_config(un, project_name, endpoint, client.org_namespace)     
      file_name = "settings.yaml"
      src = File.new(existing_location+"/"+project_name+".sublime-project", "w")
      src.puts('{"folders":[{"path": "'+existing_location+'"}],"settings":{"mm_project_directory":"'+existing_location+'"}}')
      src.close
      add_to_keychain(project_name, pw)
      threads << Thread.new {
        thread_client = MavensMate::Client.new({ 
         :sid => client.sid, 
         :metadata_server_url => client.metadata_server_url 
        })
        object_response = thread_client.list("CustomObject", true)
        object_list = []
        object_response[:list_metadata_response][:result].each do |obj|
         object_list.push(obj[:full_name])
        end 
        object_hash = { "CustomObject" => object_list }               
        options = { :meta_types => object_hash }
        object_zip = thread_client.retrieve(options) #get selected metadata
        Dir.mkdir(existing_location+"/config") unless File.exists?(existing_location+"/config") 
        MavensMate::FileFactory.put_object_metadata(project_name, object_zip)
      } 
      threads.each { |t|  t.join }
      return { :success => true, :message => "", :project_name => project_name }
    rescue Exception => e
      return { :success => false, :message => e.message }
    end
  end

  #creates new local project from salesforce metadata 
  def self.new_project(params)      
    if (params[:pn] == "" || params[:un] == "" || params[:pw] == "")
      return alert "Project Name, Salesforce Username, and Salesforce Password are all required fields!"
    end
    project_folder = get_project_folder
    project_name = params[:pn]
  	if File.directory?("#{project_folder}#{project_name}")
  	  return alert "Hm, it looks like this project already exists in your project folder. Better get more creative!"
  	end

    begin   
      un            = params[:un]
      pw            = params[:pw]
      server_url    = params[:server_url]
      vc_un         = params[:vc_un] || ""
      vc_pw         = params[:vc_pw] || ""
      vc_url        = params[:vc_url] || ""
      is_vc         = vc_url != ""                                                                                                 
      vc_alias      = params[:vc_alias] || "origin"
      vc_url.chop! if vc_url[vc_url.length-1,1] == "/" 
      vc_type       = params[:vc_type] || "SVN"
      vc_branch     = params[:vc_branch] || "master"
      vc_url        = vc_url + "/" + project_name if vc_type == "SVN" 
      endpoint      = MavensMate::Util.get_sfdc_endpoint(server_url)   
      ENV["MM_WORKSPACE"] = params[:where]
      
      client = MavensMate::Client.new({ :username => un, :password => pw, :endpoint => endpoint })

      Thread.abort_on_exception = true
      threads = []  

      MavensMate::FileFactory.put_project_directory(project_name) #put project directory in the filesystem     
      MavensMate::FileFactory.put_project_config(un, project_name, endpoint, client.org_namespace)
      MavensMate::FileFactory.put_sublime_text_project_file(project_name)
      add_to_keychain(project_name, pw)

      threads << Thread.new {          
        thread_client = MavensMate::Client.new({ 
          :sid => client.sid, 
          :metadata_server_url => client.metadata_server_url 
        })
        hash = params[:package]
        tmp_dir = Dir.tmpdir 
        MavensMate::FileFactory.put_package("#{tmp_dir}/mmpackage", binding, false)
        project_zip = thread_client.retrieve({ :package => "#{tmp_dir}/mmpackage/package.xml" })            
        MavensMate::FileFactory.put_project_metadata(project_name, project_zip) #put the metadata in the project directory    
        FileUtils.rm_rf "#{tmp_dir}/mmpackage"
      }
      threads << Thread.new {
        #put object metadata 
        thread_client = MavensMate::Client.new({ 
         :sid => client.sid, 
         :metadata_server_url => client.metadata_server_url 
        })
        object_response = thread_client.list("CustomObject", true)
        object_list = []
        object_response[:list_metadata_response][:result].each do |obj|
         object_list.push(obj[:full_name])
        end 
        object_hash = { "CustomObject" => object_list }               
        options = { :meta_types => object_hash }
        object_zip = thread_client.retrieve(options) #get selected metadata
        Dir.mkdir(project_folder+project_name+"/config") unless File.exists?(project_folder+project_name+"/config") 
        MavensMate::FileFactory.put_object_metadata(project_name, object_zip)
      } 
      threads.each { |t|  t.join }
      
      if is_vc
      	if vc_type == "SVN"
      		Dir.chdir("#{project_folder}#{project_name}")	
      		%x{svn import '#{vc_url}' --trust-server-cert --non-interactive --username #{vc_un} --password #{vc_pw} -m "initial import"}
      		Dir.chdir("#{project_folder}")	
      		%x{svn checkout --force --trust-server-cert --non-interactive #{vc_url} '#{project_name}'}      
    	  elsif vc_type == "Git"
          Dir.chdir("#{project_folder}#{project_name}")
          %x{git init}
          %x{git remote add '#{vc_alias}' '#{vc_url}'}
          %x{git add .}
          %x{git commit -m 'First import'}                                     
          vc_branch = "HEAD:#{vc_branch}" if vc_branch != "master" 
          %x{git push '#{vc_alias}' '#{vc_branch}'}
    	  end
      end
      
    rescue Exception => e
      FileUtils.rm_rf("#{project_folder}#{project_name}")
      #return { :success => false, :message => e.message + "\n\n" + e.backtrace.join("\n"), :project_name => project_name }
      return { :success => false, :body => e.message, :project_name => project_name, :body_type => "text" }
    end
    return { :success => true, :body => "", :project_name => project_name, :body_type => "text" }
  end
  
  #checks out salesforce.com project from svn, applies MavensMate nature
  def self.checkout_project(params)        
    # validate [:internet, :mm_project_folder]
    
    if params[:vc_type] == "SVN"    
      if (params[:pn].nil? || params[:un].nil? || params[:pw].nil? || params[:vc_url].nil? || params[:vc_un].nil? || params[:vc_pw].nil?)
        return alert "All fields are required to check out a project from SVN"
      end
    elsif params[:vc_type] == "Git"
      if params[:vc_url].nil?
        return alert "Please specify the Git repository URL"
      end 
    end
    
    project_folder = get_project_folder
    project_name = params[:pn]
  	if File.directory?("#{project_folder}#{project_name}")
  	  return alert "Hm, it looks like this project already exists in your project folder"
  	end
    
    begin
      #puts params.inspect + "<br/>"
      un          = params[:un]
      pw          = params[:pw]
      server_url  = params[:server_url]
      vc_un       = params[:vc_un] || ""
      vc_pw       = params[:vc_pw] || ""
      vc_url      = params[:vc_url] || ""
      vc_type     = params[:vc_type] || "SVN"
      vc_branch   = params[:vc_branch] || "master"
      endpoint    = MavensMate::Util.get_sfdc_endpoint(server_url)  
      
      Thread.abort_on_exception = true
      threads = []
    	object_zip = nil
  	  threads << Thread.new {      
        Dir.mkdir(project_folder) unless File.exists?(project_folder)
    		if vc_type == "Git"
    		  if(vc_branch.downcase == 'head')
            %x{git clone '#{vc_url}' '#{project_folder}#{project_name}'} 
          else
            branchname = vc_branch.split('/').last
            %x{git clone '#{vc_url}' -b '#{branchname}' '#{project_folder}#{project_name}'}
          end
    		elsif vc_type == "SVN"
      		Dir.mkdir("#{project_folder}#{project_name}") unless File.exists?("#{project_folder}#{project_name}")
      		Dir.chdir("#{project_folder}")
      		%x{svn checkout '#{vc_url}' '#{project_name}' --trust-server-cert --non-interactive --username #{vc_un} --password #{vc_pw}}
    		end   
  		}
  		threads << Thread.new {
  		  client = MavensMate::Client.new({ :username => un, :password => pw, :endpoint => endpoint })
        object_response = client.list("CustomObject", true)
        object_list = []
        object_response[:list_metadata_response][:result].each do |obj|
          object_list.push(obj[:full_name])
        end 
        object_hash = { "CustomObject" => object_list }               
        options = { :meta_types => object_hash }
        object_zip = client.retrieve(options) #get selected metadata
  		}
  		threads.each { |aThread|  aThread.join }
        
      client = MavensMate::Client.new({ :username => un, :password => pw, :endpoint => endpoint })
      MavensMate::FileFactory.put_project_config(un, project_name, endpoint, client.org_namespace)
      MavensMate::FileFactory.put_sublime_text_project_file(project_name)
      add_to_keychain(project_name, pw)      		        
      Dir.mkdir(project_folder+project_name+"/config") unless File.exists?(project_folder+project_name+"/config") 
      MavensMate::FileFactory.put_object_metadata(project_name, object_zip)              
    
    rescue Exception => e
      FileUtils.rm_rf("#{project_folder}#{project_name}")
      return { :success => false, :message => e.message, :project_name => project_name } 
    end
    return { :success => true, :message => "", :project_name => project_name }
  end
    
  #creates new metadata (ApexClass, ApexTrigger, ApexPage, ApexComponent)
  def self.new_metadata(options={})
    begin
      object_name     = options[:object_api_name] || ""
      apex_class_type = options[:apex_class_type] || "base"
      meta_type       = options[:meta_type]
      api_name        = options[:api_name]

      client = MavensMate::Client.new
      if client.metadata_exist?(options)
        res = { :success => false, :message => "This API name is already in use in your org" }
        puts res.to_json
        return
      end

      zip_file = MavensMate::FileFactory.put_local_metadata(
        :api_name         => api_name, 
        :meta_type        => meta_type, 
        :object_name      => object_name, 
        :dir              => "tmp", 
        :apex_class_type  => apex_class_type
      )
      result = client.deploy({
        :zip_file => zip_file, 
        :deploy_options => "<rollbackOnError>true</rollbackOnError>"
      }) 
      if ! result[:check_deploy_status_response][:result][:success]       
        puts result.inspect
      else
        zip_file = MavensMate::FileFactory.put_local_metadata(
          :api_name         => api_name, 
          :meta_type        => meta_type, 
          :object_name      => object_name, 
          :apex_class_type  => apex_class_type
        )
        #FileFactory.update_package_xml
        #MavensMate::FileFactory.put_spec_test(api_name) if meta_type == "ApexPage"
        result[:check_deploy_status_response][:result][:location] = "#{ENV["MM_CURRENT_PROJECT_DIRECTORY"]}/src/#{META_DIR_MAP[meta_type]}/#{api_name}#{META_EXT_MAP[meta_type]}"        
        puts result.to_json
      end
    rescue Exception => e
      res = { :success => false, :message => e.message + e.backtrace.join("\n") }
      puts res.to_json
    end
  end
     
  #compiles selected file(s) or active file
  def self.save(active_file=false) 
    MavensMate::logger.debug 'compiling file'
    result = nil
    begin
      if ENV["TM_FILEPATH"] == nil or ENV["TM_FILEPATH"] == ""
        res = { :success => false, :message => "Please select a valid file" }
        puts res.to_json
        return
      end

      client = MavensMate::Client.new
      if ENV["TM_FILEPATH"].end_with?("trigger") or ENV["TM_FILEPATH"].end_with?("cls")
        options = {}
        file = File.open(ENV["TM_FILEPATH"], "rb") 
        file_body = file.read
        file.close
        if ENV["TM_FILEPATH"].end_with?("trigger")
          options = {:type => "ApexTrigger", :body => file_body }
        else
          options = {:type => "ApexClass", :body => file_body }
        end
        begin
          result = client.compile_apex(options)
          puts result.to_json
          return
        rescue Exception => e
          #res = { :success => false, :message => e.message + "\n" + e.backtrace.join("\n")}
          #puts res.to_json
          #return
          #exception is OK here, let's assume we need to do a straight deploy call
        end
      end

      files_to_save = get_metadata_hash(active_file)

      #if client.has_server_conflict(files_to_save)          
        # confirmed = TextMate::UI.request_confirmation(
        # :title => "MavensMate",
        # :prompt => "One (or more) of the files you're attempting to compile has been updated by another Salesforce.com user since your last update",
        # :button1 => "That's OK, overwrite the server copy",
        # :button2 => "Nevermind")
        # return if ! confirmed  
      #end
                  
      zip_file = MavensMate::FileFactory.put_tmp_metadata(files_to_save)     
      result = client.deploy({:zip_file => zip_file, :deploy_options => "<rollbackOnError>true</rollbackOnError>"})            
      puts result.to_json
    rescue Exception => e
      res = { :success => false, :message => e.message+ "\n" + e.backtrace.join("\n") }
      #MavensMate::logger.error "error compiling"
      #MavensMate::logger.error e.message+ "\n" + e.backtrace.join("\n")
      puts res.to_json
    end
    # if ! result[:check_deploy_status_response][:result][:success]       
    #   TextMate.exit_show_html(dispatch :controller => "deploy", :action => "show_compile_result", :result => result)        
    # end
  end

  def self.execute_apex(options)
    begin
      client = MavensMate::Client.new
      result = client.execute_apex(options)
      return result
    rescue Exception => e
      return { :success => false, :body => e.message, :body_type => "text" }
    end
  end
    
  #refreshes the selected file from the server // TODO:selected *files*
  def self.refresh_selected_file     
    begin
      client = MavensMate::Client.new
      result_zip = client.retrieve({ :path => ENV['TM_FILEPATH'] }) 
      MavensMate::FileFactory.replace_file(ENV['TM_FILEPATH'], result_zip)
      res = { :success => true, :message => "Refreshed successfully" }
      puts res.to_json
    rescue Exception => e
      res = { :success => false, :message => e.message }
      puts res.to_json
    end
  end
    
  #deletes selected file(s) from the server (and locally)
  def self.delete_selected_files        
    begin
      zip_file = MavensMate::FileFactory.put_delete_metadata(get_metadata_hash)     
      client = MavensMate::Client.new
      result = client.deploy({:zip_file => zip_file, :deploy_options => "<rollbackOnError>true</rollbackOnError>"})
      if result[:check_deploy_status_response][:result][:success]       
        get_selected_files.each do |f|
          FileUtils.rm_r f   
        end
        #FileFactory.update_package_xml
        puts result.to_json
      else
        #html = dispatch :controller => "deploy", :action => "show_compile_result", :result => result
        #need to display mavensmate.app with delete result here 
        puts result.to_json 
      end
    rescue Exception => e
      res = { :success => false, :message => e.message }
      puts res.to_json 
    end
  end

  def self.compile_selected_files
    begin
      zip_file = MavensMate::FileFactory.put_tmp_metadata(get_metadata_hash)     
      client = MavensMate::Client.new
      result = client.deploy({:zip_file => zip_file, :deploy_options => "<rollbackOnError>true</rollbackOnError>"})
      puts result.to_json
    rescue Exception => e
      res = { :success => false, :message => e.message+ "\n" + e.backtrace.join("\n") }
      puts res.to_json 
    end
  end
  
  #compiles entire project
  def self.compile_project
    result = nil
    begin
      zip_file = MavensMate::FileFactory.copy_project_to_tmp     
      client = MavensMate::Client.new  
      result = client.deploy({:zip_file => zip_file, :deploy_options => "<rollbackOnError>true</rollbackOnError>"}) 
      puts result.to_json
    rescue Exception => e
      res = { :success => false, :message => e.message }
      puts res.to_json
    end  
  end

  def self.clean_dirs(options={})
    begin
      if ! options[:dirs]
        result = { :success => false, :message => "No directories specified" }
        puts result.to_json 
        return
      end
      dirs = options[:dirs].split(",")
      if dirs.size == 1 and dirs.first.split("/").last == "src"
        clean_project
        return
      end
      hash = { }
      options[:dirs].split(",").each do |dir|
        dir_base_name = dir.split("/").last
        type = MetadataHelper.get_meta_type_by_dir(dir_base_name)[:xml_name]
        hash[type] = ["*"]
      end
      threads = []
      Thread.abort_on_exception = true
      client = nil
      pd = ENV['MM_CURRENT_PROJECT_DIRECTORY']
      Dir.foreach("#{pd}/src") do |entry| #iterate the metadata folders
        next if entry.include? "."
        next if !options[:dirs].include?(entry) #skip the folder if it's not being refreshed
        Dir.foreach("#{pd}/src/#{entry}") do |subentry| #iterate the files inside those folders
          next if subentry == '.' || subentry == '..' || subentry == '.svn' || subentry == '.git'
          FileUtils.rm_r "#{pd}/src/#{entry}/#{subentry}" #delete what's inside
        end
      end
      tmp_dir = MavensMate::FileFactory.put_tmp_directory
      MavensMate::FileFactory.put_package(tmp_dir, binding, false)
      client = MavensMate::Client.new
      threads << Thread.new {
        thread_client = MavensMate::Client.new({ :sid => client.sid, :metadata_server_url => client.metadata_server_url })
        project_zip = thread_client.retrieve({ :package => tmp_dir+"/package.xml" })
        MavensMate::FileFactory.finish_clean(get_project_name, project_zip) #put the metadata in the project directory  
      }
      threads.each { |aThread|  aThread.join }                  
      result = { :success => true }
      puts result.to_json 
    rescue Exception => e
      result = { :success => false, :message => +e.message + "\n" + e.backtrace.join("\n") }
      puts result.to_json
    end
  end
        
  #wipes local project and rewrites with server copies based on current project's package.xml, preserves svn/git      
  def self.clean_project(options={})       
    begin
      File.delete("#{ENV['MM_CURRENT_PROJECT_DIRECTORY']}/src/package.xml") if options[:update_package]
      threads = []
      Thread.abort_on_exception = true
      client = nil
      pd = ENV['MM_CURRENT_PROJECT_DIRECTORY']
      Dir.foreach("#{pd}/src") do |entry| #iterate the metadata folders
        next if entry.include? "."
        Dir.foreach("#{pd}/src/#{entry}") do |subentry| #iterate the files inside those folders
          next if subentry == '.' || subentry == '..' || subentry == '.svn' || subentry == '.git'
          FileUtils.rm_r "#{pd}/src/#{entry}/#{subentry}" #delete what's inside
        end
      end
      require 'fileutils'   
      FileUtils.rm_r "#{pd}/config/objects" if File.directory? "#{pd}/config/objects"
      MavensMate::FileFactory.clean_directory("#{pd}/config/objects", ".object")        
      client = MavensMate::Client.new({:override_session => true})
      threads << Thread.new {
        thread_client = MavensMate::Client.new({ :sid => client.sid, :metadata_server_url => client.metadata_server_url })
        if options[:package]
          hash = options[:package] 
          MavensMate::FileFactory.put_package("#{ENV['MM_CURRENT_PROJECT_DIRECTORY']}/src", binding, false)
        end
        project_zip = thread_client.retrieve({ :package => "#{ENV['MM_CURRENT_PROJECT_DIRECTORY']}/src/package.xml" })
        MavensMate::FileFactory.finish_clean(get_project_name, project_zip) #put the metadata in the project directory  
      }
      if options[:update_sobjects]
        threads << Thread.new {
          thread_client = MavensMate::Client.new({ 
            :sid => client.sid, 
            :metadata_server_url => client.metadata_server_url 
          })
          object_response = thread_client.list("CustomObject", true)
          object_list = []
          object_response[:list_metadata_response][:result].each do |obj|
            object_list.push(obj[:full_name])
          end 
          object_hash = { "CustomObject" => object_list }               
          options = { :meta_types => object_hash }
          object_zip = thread_client.retrieve(options) #get selected metadata 
          Dir.mkdir("#{ENV['MM_CURRENT_PROJECT_DIRECTORY']}/config") unless File.exists?("#{ENV['MM_CURRENT_PROJECT_DIRECTORY']}/config") 
          MavensMate::FileFactory.put_object_metadata(get_project_name, object_zip)   
        }        
      end
      threads.each { |aThread|  aThread.join }                  
      result = { :success => true }
      return result if options[:force_return] 
      puts result.to_json 
    rescue Exception => e
      #alert e.message + "\n" + e.backtrace.join("\n")
      result = { :success => false, :message => +e.message + "\n" + e.backtrace.join("\n") }
      return result if options[:force_return] 
      puts result.to_json  
    end   
  end
  
  #creates a local changeset
  def self.new_changeset(options={})
    begin
      TextMate.call_with_progress( :title => "MavensMate", :message => "Creating changeset" ) do        
        Dir.mkdir("#{ENV['MM_CURRENT_PROJECT_DIRECTORY']}/changesets") unless File.exists?("#{ENV['MM_CURRENT_PROJECT_DIRECTORY']}/changesets")
        client = MavensMate::Client.new
        where = "#{ENV['MM_CURRENT_PROJECT_DIRECTORY']}/changesets/#{options[:name]}"
        hash = options[:package] 
        MavensMate::FileFactory.put_package(where, binding, false)
        project_zip = client.retrieve({ :package => "#{ENV['MM_CURRENT_PROJECT_DIRECTORY']}/changesets/#{options[:name]}/package.xml" })
        MavensMate::FileFactory.extract(project_zip, where)
        TextMate.rescan_project
        FileUtils.rm_rf "#{ENV['MM_CURRENT_PROJECT_DIRECTORY']}/changesets/#{options[:name]}/package.xml"
        return { :success => true, :message => "" }
      end
    rescue
      return { :success => false, :message => e.message }
    end
  end
    
  #deploys project metadata to a salesforce.com server
  def self.deploy_to_server(params)
    begin
      endpoint = MavensMate::Util.get_sfdc_endpoint_by_type(params[:endpoint_type])
      tmp_dir = MavensMate::FileFactory.put_tmp_directory
      client = MavensMate::Client.new
      if params[:package_type] == "Custom"
        hash = params[:package]
        deploy = true
        MavensMate::FileFactory.put_package(tmp_dir, binding, false)
        zip_file = client.retrieve({ :package => "#{tmp_dir}/package.xml" })
      else
        zip_file = client.retrieve({ :package => "#{ENV['MM_CURRENT_PROJECT_DIRECTORY']}/changesets/#{params[:changeset]}/unpackaged/package.xml" })
      end                
      client = MavensMate::Client.new({ :username => params[:un], :password => params[:pw], :endpoint => endpoint, :override_session => true })
      result = client.deploy({
        :zip_file => zip_file,
        :deploy_options => "<checkOnly>#{params[:check_only]}</checkOnly><rollbackOnError>true</rollbackOnError>"
      })
      MavensMate::FileFactory.remove_directory(tmp_dir) unless params[:package_type] != "Custom"
      return result
    rescue Exception => e
      MavensMate::FileFactory.remove_directory(tmp_dir)
      result = { :success => false, :message => e.message + "\n" + e.backtrace.join("\n") }
      #result = { :success => false, :message => e.message }
      return result
    end
  end
  
  def self.diff(params)
    hash = params[:package]
    deploy = true
    tmp_dir = Dir.tmpdir
    MavensMate::FileFactory.put_package(tmp_dir, binding, false)    
    tmp = MavensMate::FileFactory.put_tmp_directory
    
    project_user = get_project_config['username']
    
    compare_dict = { }
        
    Thread.abort_on_exception = true
    threads = [] 
    params[:orgs].each do |org|
      threads << Thread.new { 
        thread_client = MavensMate::Client.new({ :username => org[:un], :password => org[:pw], :endpoint => org[:endpoint] })      
        zip_file = thread_client.retrieve({ :package => "#{tmp_dir}/package.xml" })  
        Dir.mkdir("#{tmp}/#{org[:un]}")
        MavensMate::FileFactory.extract(zip_file, "#{tmp}/#{org[:un]}")
        compare_dict[org[:un]] = { :matches => false, :location => "" }
      } 
    end
    threads << Thread.new {
      client = MavensMate::Client.new      
      zip_file = client.retrieve({ :package => "#{tmp_dir}/package.xml" })  
      Dir.mkdir("#{tmp}/#{project_user}")
      MavensMate::FileFactory.extract(zip_file, "#{tmp}/#{project_user}")
    } 
    threads.each { |aThread|  aThread.join }
    
    
    #compile list of origin metadata
    dict = { }
    Dir.foreach("#{tmp}/#{project_user}/unpackaged") do |mf|
      next if mf == "." or mf == ".." or mf == "package.xml"
      Dir.foreach("#{tmp}/#{project_user}/unpackaged/#{mf}") do |item|
        next if item == "." or item == ".." or item.include? "-meta.xml"
        bn = File.basename("#{tmp}/#{project_user}/unpackaged/#{mf}/#{item}")        
        dict[bn] = { :origin_username => project_user, :origin_location => "#{tmp}/#{project_user}/unpackaged/#{mf}/#{item}", :compare_to => compare_dict }
      end
    end
    
    #puts dict.inspect
    
    # {
    #     "CompileAndTest.cls"=>{
    #       "compare_to"=> {
    #         "joeferraro@force.com"=>{}, 
    #         "joeferraro2@force.com"=>{}
    #       }, 
    #       :origin_location=>"/var/folders/m3/kt10_j3j5417w5xvxxywdj080000gp/T/.org.mavens.mavensmate.gcfxLLkyc/joeferraro3@force.com/unpackaged/classes/CompileAndTest.cls"
    #     }, 
    #     "Account-Account Layout.layout"=>{
    #       "compare_to"=> {
    #         "joeferraro@force.com"=>{}, 
    #         "joeferraro2@force.com"=>{}
    #       }, 
    #       :origin_location=>"/var/folders/m3/kt10_j3j5417w5xvxxywdj080000gp/T/.org.mavens.mavensmate.gcfxLLkyc/joeferraro3@force.com/unpackaged/layouts/Account-Account Layout.layout"
    #     }
    # }
    
    #FileUtils.rm_rf "#{tmp}/#{project_user}"   
    #puts origin_list.inspect #=> ["/users/foo/projects/bar.cls", "another file"]
        
    dict.each { |basename, v|
      puts "basename is: " + basename
      matches = Dir["#{tmp}/**/*#{basename}"]
      matches.each do |m|
        arr = m.split("/")
        un = arr[arr.index("unpackaged") - 1]
        next if dict[basename][:origin_username] == un
        puts "match: " + m
        # puts dict[basename].inspect
        # puts dict[basename][:compare_to].inspect
        # puts dict[basename][:compare_to][un].inspect
        dict[basename][:compare_to][un][:matches] = is_match(dict[basename][:origin_location], m)
        dict[basename][:compare_to][un][:location] = m
      end
      puts "\n\n" + dict.inspect + "\n\n"
    }
    
    puts "\n\n\n\n\n\n"
    puts dict.inspect
          
  end
  
  def self.is_match(file1_path, file2_path)
    is_match = false
    begin  
      is_match = FileUtils.compare_file(file1_path, file2_path)
    rescue Exception => e
      puts "no such file: " + e.message
      is_match = false if e.message.include? "No such file or directory"
    end
    return is_match 
  end
  
  #runs apex tests in selected class
  def self.run_tests(tests, debug_options, api)
    if api == "apex"
      begin
        client = MavensMate::Client.new
        result = client.run_tests(tests, debug_options)
        return result
      rescue Exception => e
        return e.message
      end 
    else
      run_test_body = ""
      tests.each do |t|
        run_test_body << "<runTests>#{t}</runTests>"
      end    
      run_test_body << "<rollbackOnError>true</rollbackOnError>" 
      begin
        zip_file = MavensMate::FileFactory.put_empty_metadata    
        client = MavensMate::Client.new
        result = client.deploy({:zip_file => zip_file, :deploy_options => run_test_body, :debug_options => debug_options })
        return result      
      rescue Exception => e
        return e.message
      end
    end   
  end
      
  #returns the project name
  def self.get_project_name
    yml = YAML::load(File.open(ENV['MM_CURRENT_PROJECT_DIRECTORY'] + "/config/settings.yaml"))
    project_name = yml['project_name']
  end
  
  #returns yaml project settings
  def self.get_project_config
    return YAML::load(File.open(ENV['MM_CURRENT_PROJECT_DIRECTORY'] + "/config/settings.yaml"))
  end
  
  #builds server index and stores in .org_metadata
  def self.build_index
    mhash = eval(File.read("#{SUPPORT}/conf/metadata_dictionary"))
    mhash.sort! { |a,b| a[:xml_name].downcase <=> b[:xml_name].downcase } 
    project_array = []
    progress = 0
    threads = []            
    client = MavensMate::Client.new
    mhash.each do |metadata|         
      threads << Thread.new {
        thread_client = MavensMate::Client.new({ :sid => client.sid, :metadata_server_url => client.metadata_server_url })
        begin   
          project_array.push({
            :title => metadata[:xml_name],
            :key => metadata[:xml_name],
            :isLazy => false,
            :isFolder => true,
            :selected => false,
            :children => thread_client.list(metadata[:xml_name], false, "array"),
            :inFolder => metadata[:in_folder],
            :hasChildTypes => metadata[:child_xml_names] ? true : false
          })
        rescue  Exception => e
          puts e.message + "\n" + e.backtrace.join("\n")  
        end
      }        
    end
    threads.each { |aThread|  aThread.join }
    project_array.sort! { |a,b| a[:title].downcase <=> b[:title].downcase }
    File.open("#{ENV['MM_CURRENT_PROJECT_DIRECTORY']}/config/.org_metadata", 'w') {|f| f.write(project_array.inspect) }
    return project_array
  end

  def self.file_ready
    return false
    begin
      f = File.open("#{ENV['MM_CURRENT_PROJECT_DIRECTORY']}/config/.org_metadata", 'r')
      return true
    rescue
      return false
    end
  end
  
  #selects all metadata in tree
  def self.select_all(obj)
    begin
      obj[:children].each do |child|
        child[:selected] = "selected"
        next if ! child[:children]
        child[:children].each do |grand_child|
          grand_child[:selected] = "selected"
          next if ! grand_child[:children]
          grand_child[:children].each do |great_grand_child|
            great_grand_child[:selected] = "selected"
          end
        end
      end
    rescue

    end
  end
    
  def self.close_deploy_window
    pid = fork do
      Thread.new do
        script_path = "#{ENV['TM_BUNDLE_SUPPORT']}/osx/closedeploywindow.scpt"
        %x{osascript &>/dev/null '#{script_path}'}
      end
    end
    Process.detach(pid)
  end
  
  #adds salesforce.com creds to the keychain
  def self.add_to_keychain(project_name, pw)
    require 'shellwords'
    pw = Shellwords.escape(pw)
    project_name = Shellwords.escape(project_name) + "-mm"
    %x{security add-generic-password -a #{project_name} -s \"MavensMate: #{project_name}\" -w #{pw} -U}
  end
  
  #returns the selected location of projects
  def self.get_project_folder
    project_folder = ENV['MM_WORKSPACE']
  	project_folder +='/' unless project_folder.end_with?("/")
  end

  def self.get_org_connections
    connections = []
    begin
      pconfig = MavensMate.get_project_config
      pconfig['org_connections'].each do |connection| 
        pw = KeyChain::find_internet_password("#{pconfig['project_name']}-mm-#{connection['name']}")
        connections.push({
          :un => connection["username"], 
          :pw => pw
        })
      end 
    rescue      
    end
    return connections
  end
  
  private
    
    #returns a list of apex methods based on the object and method type supplied    
    def self.apex_methods(options={})
      require 'yaml'
      methods = []
      yml = YAML::load(File.open("#{ENV['TM_BUNDLE_SUPPORT']}/lib/apex/#{options[:object]}.yaml"))
      yml[options[:method_type]].each do |method|
        methods.push(method)
      end
      return methods
    end
    
    #validates textmate command
    def self.validate(options=[])
      if options.include?(:internet)
        if ! has_internet
          return alert "You don't seem to have an active internet connection!"
        end
      end
      if options.include?(:mm_project)
        if ! is_mm_project
          return alert "This doesn't seem to be a valid MavensMate project"
        end
      end
      if options.include?(:run_test)
        if ! File.extname(".cls")
          return alert "This doesn't seem to be a valid Apex Class file" 
        end
      end
      if options.include?(:file_selected)
        if ENV['TM_FILEPATH'].nil?
          return alert "Please select a file to refresh from the server"
        end
      end
      if options.include?(:mm_project_folder)
        if ENV['MM_WORKSPACE'].nil?
          return alert "Please specify your projects folder by setting 'mm_workspace' in Preferences.sublime-settings"
        end
      end
    end
    
    #creates a UI alert with the specified message
    def self.alert(message)
      return { :success => false, :body => message }
    end
    
    #returns the name of a file without its extension
    def self.get_name_no_extension(name)
      return name.split(".")[0]
    end
            
    #returns metadata hash of selected files  #=> {"ApexClass" => ["aclass", "anotherclass"], "ApexTrigger" => ["atrigger", "anothertrigger"]}
    def self.get_metadata_hash(active_file=false)
      selected_files = get_selected_files(active_file)     
      MavensMate::logger.debug 'selected_files: ' + selected_files.inspect
      meta_hash = {}
      selected_files.each do |f|
        #puts "selected file: " + f + "\n\n"
        next if ! f.include? "." #need files only, not directories
        next if f.include? "-meta.xml" #dont need meta files
        ext = File.extname(f) #=> .cls
        ext_no_period = File.extname(f).gsub(".","") #=> cls
        metadata_definition = MavensMate::FileFactory.get_meta_type_by_suffix(ext_no_period)      
        meta_type = metadata_definition[:xml_name]
        #puts "meta_type: " + meta_type.inspect + "<br/>"

        if ! meta_hash.key? meta_type #key isn't there yet, put it in        
          if metadata_definition[:in_folder]
            arr = f.split("/")
            if arr[arr.length-2] != metadata_definition[:directory_name]
              meta_hash[meta_type] = [arr[arr.length-2]+"/"+File.basename(f, ext)] #file name with no extension
            else
              meta_hash[meta_type] = [File.basename(f, ext)] #file name with no extension
            end
          else
            meta_hash[meta_type] = [File.basename(f, ext)] #file name with no extension
          end
        else #key is there, let's add metadata to it
          meta_array = meta_hash[meta_type] #get the existing array
          if metadata_definition[:in_folder]
            arr = f.split("/")
            if arr[arr.length-2] != metadata_definition[:directory_name]
              meta_array.push(arr[arr.length-2]+"/"+File.basename(f, ext)) #file name with no extension
            else
              meta_array.push(File.basename(f, ext)) #add the new piece of metadata
            end
          else
            meta_array.push(File.basename(f, ext)) #file name with no extension
          end
          #meta_array.push(File.basename(f, ext)) #add the new piece of metadata
          meta_hash[meta_type] = meta_array #replace the key
        end 
      end
            
      #puts "hash is: "+meta_hash.inspect      
      return meta_hash
    end
        
    #returns array of selected files #=> ["/users/username/projects/foo/classes/myclass123.cls", /users/username/projects/foo/classes/myclass345.cls"]
    def self.get_selected_files(active_file=false)
      if active_file
        return Array[ENV['TM_FILEPATH']]
      else
        begin
          selected_files = ENV["TM_SELECTED_FILES"].split(",")
          MavensMate::logger.debug 'selected_files: ' + selected_files.inspect
          #puts selected_files.inspect
          #selected_files = Shellwords.shellwords(ENV["TM_SELECTED_FILES"])
          selected_files.each do |f|
            MavensMate::logger.debug 'file: ' + f
            next if f.include? "-meta.xml"        
            ext = File.extname(f).gsub(".","") #=> cls
            MavensMate::logger.debug 'ext: ' + ext
            mt_hash = MavensMate::FileFactory.get_meta_type_by_suffix(ext)      
            if mt_hash == nil
              selected_files.delete(f)
              next
            end
            if mt_hash[:meta_file]
              if ! selected_files.include? f + "-meta.xml" #if they didn't select the meta file, select it anyway
                selected_files.push(f + "-meta.xml")   
              end
            end
          end
          MavensMate::logger.debug 'selected_files: ' + selected_files.inspect
          selected_files.uniq!
          return selected_files
        rescue Exception => e
          #puts e.backtrace
          MavensMate::logger.debug 'error: ' + e.message + e.backtrace.join("\n") 
          return Array[ENV['TM_FILEPATH']]
        end
      end
    end
                    
    #pings google.com to determine whether there's an active internet connection
    def self.has_internet
      require 'socket' 
      begin 
        if ENV["http_proxy"]
          TCPSocket.new URI.parse(ENV["http_proxy"]).host, URI.parse(ENV["http_proxy"]).port 
        else
          TCPSocket.new 'google.com', 80 
        end   
      rescue SocketError 
        return false 
      end
      return true
    end
    
    #determines whether this is a mavensmate project
    def self.is_mm_project
      project_dir = ENV['MM_CURRENT_PROJECT_DIRECTORY'] + "/config"
      config_file = ENV['MM_CURRENT_PROJECT_DIRECTORY'] + "/config/settings.yaml"
      if ! File.directory?(project_dir) && ! File.exists?(config_file)
    	  return false
      end
      return true
    end

end