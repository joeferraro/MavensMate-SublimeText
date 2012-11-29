# encoding: utf-8
require 'rubygems'
require 'thin'
require 'json'
require File.dirname(File.dirname(File.dirname(__FILE__))) + "/constants.rb"
include Constants
require File.dirname(__FILE__) + '/keychain.rb'
require File.dirname(__FILE__) + '/lsof.rb'
require File.dirname(__FILE__) + '/object.rb'
require File.dirname(__FILE__) + '/mavensmate.rb'

module MavensMate
  module LocalServerThin
      
      class << self
        
        def get_server_config
          server = Rack::URLMap.new(
              '/project'           => ProjectServlet.new, 
              '/project/edit'      => ProjectEditServlet.new, 
              '/project/existing'  => ExistingProjectServlet.new, 
              '/metadata/list'     => MetadataListServlet.new, 
              '/vc'                => VersionControlServlet.new, 
              '/auth'              => AuthenticationServlet.new, 
              '/test'              => ApexUnitTestServlet.new, 
              '/metadata/index'    => MetadataIndexServlet.new, 
              '/deploy'            => DeployServlet.new, 
              '/execute'           => ExecuteApexServlet.new, 
              '/connections'       => OrgConnectionServlet.new,
              '/status'            => RequestStatusServlet.new
            )
          return server
        end

        def start_test
          stop
          server = MavensMate::LocalServerThin.get_server_config 
          Thin::Server.new('0.0.0.0', 7777, server).start!
        end

        def start
          stop
          MavensMate::logger.debug 'thin server starting on port 7777'
          exit if fork            # Parent exits, child continues.
          Process.setsid          # Become session leader.
          exit if fork            # Zap session leader.

          pid = fork do
            server = MavensMate::LocalServerThin.get_server_config 
            Thin::Server.new('0.0.0.0', 7777, server).start!
          end
          Process.detach(pid)
        end

        def respond(body, type)
          MavensMate::logger.debug 'responding from localhost:7777\n'+body
          [
            200,
            { 'Content-Type' => type, 'Access-Control-Allow-Origin' => "*" },
            body
          ]
        end

        def stop
          MavensMate::logger.debug 'shutting down server running on port 7777'
          if Lsof.running?(7125)
            Lsof.kill(7125)
          end
          if Lsof.running?(7777)
            Lsof.kill(7777)
          end          
        end

        #client polls this servlet to determine whether the request is done
        #if the request IS done, it will respond with the body of the request
        class RequestStatusServlet
          def call(env)
            req = Rack::Request.new(env)
            begin
              if MavensMate::FileFactory.response_ready?(req["id"])
                json = File.read(MavensMate::FileFactory.get_tmp_response_file(req["id"]))
                MavensMate::FileFactory.remove_directory(File.dirname(MavensMate::FileFactory.get_tmp_response_file(req["id"])))
                MavensMate::LocalServerThin.respond(json, 'text/json')
              else
                result = {
                  :status => "pending",
                  :id     => req["id"]
                }
                MavensMate::LocalServerThin.respond(result.to_json, 'text/json')
              end
            rescue Exception => e
                result = {
                  :status   => "error",
                  :id       => req["id"],
                  :message  => e.message + e.backtrace.join("\n")
                }
                MavensMate::LocalServerThin.respond(result.to_json, 'text/json')
            end
          end 
        end

        class AuthenticationServlet
          def call(env)            
            req = Rack::Request.new(env)
            request_id, tmp_directory = MavensMate::FileFactory.get_request_id_and_put_tmp_directory
            MavensMate::logger.debug 'AuthenticationServlet: ' + req.inspect
            Thread.new {
              begin              
                update_creds = req["update_creds"] || false
                sid = nil
                murl = nil
                client = MavensMate::Client.new({ 
                  :username => req["un"], 
                  :password => req["pw"], 
                  :endpoint => req["server_url"], 
                  :override_session => req["override_session"] || false
                })
                
                if ! client.sid.nil? && ! client.metadata_server_url.nil?
                  if update_creds
                    if RUBY_VERSION =~ /1.9/
                      Encoding.default_external = Encoding::UTF_8
                      Encoding.default_internal = Encoding::UTF_8
                    end
                    ENV['MM_CURRENT_PROJECT_DIRECTORY'] = req["pd"].to_s
                    un = req["un"].to_s
                    pw = req["pw"].to_s
                    server_url = req["server_url"].to_s
                    environment = (server_url.include? "test") ? "sandbox" : "production"
                    require 'yaml'
                    yml = YAML::load(File.open("#{ENV['MM_CURRENT_PROJECT_DIRECTORY']}/config/settings.yaml")) 
                    project_name = yml['project_name'].to_s
                    yml['username'] = un
                    yml['environment'] = environment 
                    File.open("#{ENV['MM_CURRENT_PROJECT_DIRECTORY']}/config/settings.yaml", 'w') { |f| YAML.dump(yml, f) }
                    MavensMate.add_to_keychain(project_name, pw)
                    FileUtils.rm_r("#{ENV['MM_CURRENT_PROJECT_DIRECTORY']}/config/.session") if File.exist?("#{ENV['MM_CURRENT_PROJECT_DIRECTORY']}/config/.session")
                    result = {
                      :success    => true,
                      :body       => "Credentials successfully updated!",
                      :body_type  => "text"
                    }
                    body = result.to_json
                  else
                    result = {
                      :success  => true, 
                      :sid      => client.sid, 
                      :murl     => client.metadata_server_url 
                    }
                    body = result.to_json
                  end
                end
              rescue Exception => e
                  result = {
                    :success    => false, 
                    :body       => e.message,
                    :body_type  => "text" 
                  }
                  body = result.to_json
              end
              File.open("#{tmp_directory}/.response", 'w') {|f| f.write(body) }
            }
            MavensMate::LocalServerThin.respond_with_async_request_id(request_id)
          end    
        end
        
        class ExecuteApexServlet
          def call(env)
            req = Rack::Request.new(env)
            request_id, tmp_directory = MavensMate::FileFactory.get_request_id_and_put_tmp_directory
            Thread.new {
              begin
                ENV["MM_CURRENT_PROJECT_DIRECTORY"] = req["mm_current_project_directory"]                
                options = {
                  :level => req["level"],
                  :category => req["category"],
                  :body => MavensMate::Util.soap_escape(req["body"])
                }
                result = MavensMate.execute_apex(options)
                body = result.to_json
              rescue Exception => e
                result = {
                    :success    => false, 
                    :body       => e.message + e.backtrace.join("\n"),
                    :body_type  => "text" 
                }
                body = result.to_json
              end
              File.open("#{tmp_directory}/.response", 'w') {|f| f.write(body) }
            }
            MavensMate::LocalServerThin.respond_with_async_request_id(request_id)
          end
        end

        class ApexUnitTestServlet
          def call(env)
            req = Rack::Request.new(env)
            request_id, tmp_directory = MavensMate::FileFactory.get_request_id_and_put_tmp_directory
            Thread.new {
              body = ""
              ENV["MM_CURRENT_PROJECT_DIRECTORY"] = req["mm_current_project_directory"]
              require SUPPORT + "/environment.rb"
              require File.dirname(File.dirname(File.dirname(__FILE__))) + "/support/tmvc/lib/application_controller.rb"
              test_result = {}
              debug_options = {
                :level => req["level"],
                :category => req["category"]
              }
              api = req["api"]
              begin
                result = MavensMate.run_tests(req["selected_tests"].split(","), debug_options, api)
                if result[:run_tests_response] || result[:check_deploy_status_response]
                  ac = ApplicationController.new
                  if RUBY_VERSION =~ /1.9/
                    Encoding.default_external = Encoding::UTF_8
                    Encoding.default_internal = Encoding::UTF_8
                  end 
                  if api == "apex"
                    html = ac.render_to_string "unit_test/_test_result", :locals => { :result => result }
                  else
                    html = ac.render_to_string "unit_test/_test_result_metadata_api", :locals => { :result => result }
                  end
                  result = {
                    :success    => true,
                    :body       => html,
                    :body_type  => "html"
                  }
                  body = result.to_json
                else
                  result = {
                    :success    => false,
                    :body       => result.inspect,
                    :body_type  => "text"
                  }
                  body = result.to_json
                end
              rescue Exception => e
                result = {
                    :success  => false, 
                    :message  => e.message + e.backtrace.join("\n") + "<br/>" + result.inspect
                }
                body = result.to_json
              end
              File.open("#{tmp_directory}/.response", 'w') {|f| f.write(body) }
            }
            MavensMate::LocalServerThin.respond_with_async_request_id(request_id)
          end
        end

        #indexes server metadata to the .org_metadata file in the project config folder
        class MetadataIndexServlet
          def call(env)            
            req = Rack::Request.new(env)
            request_id, tmp_directory = MavensMate::FileFactory.get_request_id_and_put_tmp_directory
            Thread.new {
              body = ""
              begin              
                if RUBY_VERSION =~ /1.9/
                  Encoding.default_external = Encoding::UTF_8
                  Encoding.default_internal = Encoding::UTF_8
                end
                #resp['Content-Type'] = 'html'
                
                ENV["MM_CURRENT_PROJECT_DIRECTORY"] = req["mm_current_project_directory"]
                mode = req["mode"] || ""
                do_refresh = req["do_refresh"]
                metadata_array = nil
                if do_refresh == "true" or do_refresh == true
                  metadata_array = MavensMate.build_index
                else
                  metadata_array = eval(File.read("#{ENV['MM_CURRENT_PROJECT_DIRECTORY']}/config/.org_metadata")) #=> comprehensive list of server metadata    
                end
                if mode == "edit"
                  require 'rubygems'
                  require 'nokogiri'
                  project_package = Nokogiri::XML(File.open("#{ENV['MM_CURRENT_PROJECT_DIRECTORY']}/src/package.xml"))
                  project_package.remove_namespaces!
                  project_package.xpath("//types/name").each do |node|
                    object_definition = MavensMate::FileFactory.get_meta_type_by_name(node.text) || MavensMate::FileFactory.get_child_meta_type_by_name(node.text)  
                    #=> ApexClass
                    is_parent = !object_definition[:parent_xml_name]
                    server_object = metadata_array.detect { |f| f[:key] == node.text }
                    next if server_object.nil? && is_parent
                          
                    if is_parent
                      server_object[:selected] = "selected"
                      server_object[:select_mode] = (node.previous_element.text == "*") ? "all" : "some"
                      MavensMate.select_all(server_object) if server_object[:select_mode] == "all"
                      next if server_object[:selected] == "all"     
                    end
                    
                    if not is_parent
                      #=> CustomField
                      puts "not parent"
                      parent_object_definition = MavensMate::FileFactory.get_meta_type_by_name(object_definition[:parent_xml_name]) #=> CustomObject
                      prev_node = node.previous_element    
                      while prev_node.not.nil? && prev_node.node_name == "members"
                        next if prev_node.text.not.include? "."
                        obj_name = prev_node.text.split(".")[0] #=> Lead
                        obj_attribute = prev_node.text.split(".")[1] #=> Field_Name__c
                         
                        server_object = metadata_array.detect { |f| f[:key] == object_definition[:parent_xml_name] } #=> CustomObject
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
                end
                ac = ApplicationController.new
                html = ac.render_to_string "deploy/_metadata_tree", :locals => { :metadata_array => metadata_array, :mode => mode }
                result = {
                  :success    => true,
                  :body       => html,
                  :body_type  => "html"
                }
                body = result.to_json
              rescue Exception => e
                  result = {
                    :success  => false, 
                    :message  => e.message + "\n\n" + e.backtrace.join("\n")
                  }
                  body = result.to_json
              end
              File.open("#{tmp_directory}/.response", 'w') {|f| f.write(body) }
            }
            MavensMate::LocalServerThin.respond_with_async_request_id(request_id)
          end    
        end

        class DeployServlet
          def call(env)    
            req = Rack::Request.new(env)
            request_id, tmp_directory = MavensMate::FileFactory.get_request_id_and_put_tmp_directory
            Thread.new {
              body = ""
              begin              
                response = ''
                ENV["MM_CURRENT_PROJECT_DIRECTORY"] = req["mm_current_project_directory"]
                targets = JSON.parse(req["targets"].to_s)
                connections = []
                deploy_targets = []
                pconfig = MavensMate.get_project_config
                pconfig['org_connections'].each do |connection| 
                  pw = KeyChain::find_internet_password("#{pconfig['project_name']}-mm-#{connection['username']}")
                  server_url = connection["environment"] == "production" ? "https://www.salesforce.com" : "https://test.salesforce.com" 
                  connections.push({
                    :un => connection["username"], 
                    :pw => pw,
                    :server_url => server_url,
                    :type => connection["environment"]
                  })
                end

                targets.each do |t|
                  un = t["username"]
                  type = t["type"]
                  c = connections.detect { |c| c[:un] == un and c[:type] == type }
                  deploy_targets.push(c)
                end

                Thread.abort_on_exception = true
                threads = []
                tree = eval(req["tree"].to_s)
                is_check_only = req["check_only"]

                deploy_targets.each do |t|
                  threads << Thread.new {
                    params = {}
                    params[:un]            = t[:un]
                    params[:pw]            = t[:pw]
                    params[:endpoint_type] = t[:type]
                    params[:package]       = tree
                    params[:check_only]    = is_check_only
                    params[:package_type]  = "Custom"
                    deploy_result = MavensMate.deploy_to_server(params)
                    html = nil
                    begin
                      result = MavensMate::Util.parse_deploy_response(deploy_result)
                      ac = ApplicationController.new
                      html = ac.render_to_string "deploy/_deploy_result", :locals => { :result => result, :is_check_only => params[:check_only], :target_username => t[:un] }
                    rescue
                      html = '<div id="error_message" class="alert-message error"><p><strong>Deployment Failed!</strong></p><p>'+deploy_result[:message]+'</p></div> '
                    end
                    response << html
                  }
                end
                threads.each { |t|  t.join }
                ac = ApplicationController.new
                html_payload = ac.render_to_string "deploy/_deploy_target_tabs", :locals => { :deploy_result_html => response, :targets => deploy_targets }
                result = {
                  :success    => true,
                  :body       => html_payload,
                  :body_type  => "html"
                }
                body = result.to_json
              rescue Exception => e
                result = {
                    :success    => false, 
                    :body       => '<div id="error_message" class="alert-message error"><p><strong>Deployment Failed!</strong></p><p>'+e.message + e.backtrace.join("\n")+'</p></div>',
                    :body_type  => "html"
                }
                body = result.to_json
              end
              File.open("#{tmp_directory}/.response", 'w') {|f| f.write(body) }
            }
            MavensMate::LocalServerThin.respond_with_async_request_id(request_id)
          end
        end

        #TODO: not async...does it need to be?
        class ExistingProjectServlet
          def call(env)            
            req = Rack::Request.new(env)
            begin
              params = {}
              params[:pn]                 = req["pn"]
              params[:un]                 = req["un"]
              params[:pw]                 = req["pw"]
              params[:server_url]         = req["server_url"]
              params[:existing_location]  = req["existing_location"] 
              ENV["MM_WORKSPACE"]         = req["where"]
              
              result = MavensMate.new_project_from_existing_directory(params)
              if result[:success] == true
                project_file = File.join(ENV['MM_WORKSPACE'], params[:pn], params[:pn]+".sublime-project")
                `killAll MavensMate` 
                # `'/Applications/Sublime Text 2.app/Contents/SharedSupport/bin/subl' --project '#{ENV["MM_WORKSPACE"]}/#{params[:pn]}/#{params[:pn]}.sublime-project'` if result[:success]
              else
                body = result.to_json
              end
            rescue Exception => e
              puts e.message
              body = e.message.to_json
            end
            MavensMate::LocalServerThin.respond(body, 'text/json')
          end
        end
        
        class ProjectServlet
          def call(env)            
            req = Rack::Request.new(env)
            request_id, tmp_directory = MavensMate::FileFactory.get_request_id_and_put_tmp_directory
            Thread.new {
              body = ""
              begin
                params = {}
                params[:action]     = req["action"]
                params[:pn]         = req["pn"]
                params[:un]         = req["un"]
                params[:pw]         = req["pw"]
                params[:server_url] = req["server_url"]
                params[:vc_un]      = req["vc_un"]
                params[:vc_pw]      = req["vc_pw"]
                params[:vc_url]     = req["vc_url"]
                params[:vc_type]    = req["vc_type"]
                params[:vc_alias]   = req["vc_alias"]
                params[:vc_branch]  = req["vc_branch"]
                params[:package]    = eval(req["tree"]) if params[:action] == "new"
                params[:where]      = req["where"] 
                ENV["MM_WORKSPACE"] = req["where"]
                
                if params[:action] == "checkout"
                  result = MavensMate.checkout_project(params)
                else
                  result = MavensMate.new_project(params)
                end
                if result[:success]
                  body = result.to_json
                  res = {
                    :success    => true, 
                    :body       => "project created successfully",
                    :body_type  => "text"
                  }
                  body = res.to_json
                  project_file = File.join(ENV['MM_WORKSPACE'], params[:pn], params[:pn]+".sublime-project")
                  `killAll MavensMate` 
                  `'/Applications/Sublime Text 2.app/Contents/SharedSupport/bin/subl' --project '#{project_file}'`
                else
                  body = result.to_json
                end
              rescue Exception => e
                res = {
                  :success    => false, 
                  :body       => e.message + "\n\n" + e.backtrace.join("\n"),
                  :body_type  => "text"
                }
                body = res.to_json
              end
              File.open("#{tmp_directory}/.response", 'w') {|f| f.write(body) }
            }
            MavensMate::LocalServerThin.respond_with_async_request_id(request_id)
          end
        end

        #TODO: not async...does it need to be?
        class OrgConnectionServlet
          def call(env)
            req = Rack::Request.new(env)
            body = ""
            if env["REQUEST_METHOD"] == "POST"
              begin
                un = req["un"].to_s
                pw = req["pw"].to_s
                server_url = req["server_url"].to_s
                client = MavensMate::Client.new({ 
                  :username => req["un"], 
                  :password => req["pw"], 
                  :endpoint => req["server_url"], 
                  :override_session => true
                })
                project_directory = req["pd"].to_s
                ENV['MM_CURRENT_PROJECT_DIRECTORY'] = project_directory
                environment = MavensMate::Util.get_endpoint_type_by_short_url(server_url)
                require 'yaml'
                yml = YAML::load(File.open("#{project_directory}/config/settings.yaml")) 
                project_name = yml['project_name']      
                connections = []
                if yml["org_connections"]
                  connections = yml["org_connections"]
                  keychain_name = project_name + "-mm-"
                  %x{security add-generic-password -a '#{project_name}-mm-#{un}' -s \"#{project_name}-mm-#{un}\" -w #{pw} -U}         
                  connections.push({ "username" => un, "environment" => environment })
                else
                  %x{security add-generic-password -a '#{project_name}-mm-#{un}' -s \"#{project_name}-mm-#{un}\" -w #{pw} -U} 
                  yml["org_connections"] = [{ "username" => un, "environment" => environment }]
                  connections.push({ "username" => un, "environment" => environment })
                end  
                File.open("#{project_directory}/config/settings.yaml", 'w') { |f| YAML.dump(yml, f) }
                #resp['Content-Type'] = 'json'
                
                ac = ApplicationController.new
                connections = MavensMate.get_org_connections 
                html = ac.render_to_string "org_connection/_connections", :locals => { :connections => connections }
                result = {
                  :success  => true,
                  :message => html
                }
                body = result.to_json
              rescue Exception => e
                html = '<div id="error_message" class="alert-message error"><p><strong>Error!</strong></p><p>'+e.message+'</p></div> '
                result = {
                  :success  => false,
                  :message => html
                }
                body = result.to_json
              end
            else
              begin
                un = req["un"].to_s
                require 'yaml'
                project_directory = req["pd"].to_s
                ENV['MM_CURRENT_PROJECT_DIRECTORY'] = project_directory
                yml = YAML::load(File.open("#{project_directory}/config/settings.yaml")) 
                project_name = yml['project_name']      
                conns = nil
                if yml["org_connections"]
                  conns = yml["org_connections"]
                  conns.delete_if{|conn| conn["username"] == un }
                  yml["org_connections"] = conns
                end
                File.open("#{project_directory}/config/settings.yaml", 'w') { |f| YAML.dump(yml, f) } 
                #resp['Content-Type'] = 'json'
                
                ac = ApplicationController.new
                connections = MavensMate.get_org_connections 
                html = ac.render_to_string "org_connection/_connections", :locals => { :connections => connections }
                result = {
                  :success  => true,
                  :message => html
                }
                body = result.to_json
              rescue Exception => e
                html = '<div id="error_message" class="alert-message error"><p><strong>Error!</strong></p><p>'+e.message+'</p></div> '
                result = {
                  :success  => false,
                  :message => html
                }
                body = result.to_json 
              end
            end
            MavensMate::LocalServerThin.respond(body, 'text/json')
          end
        end

        class ProjectEditServlet
          def call(env)            
            req = Rack::Request.new(env)
            request_id, tmp_directory = MavensMate::FileFactory.get_request_id_and_put_tmp_directory
            Thread.new {
              begin
                tree = eval(req["tree"])  
                result = MavensMate.clean_project({ :update_sobjects => false, :update_package => true, :package => tree, :force_return => true })
                if result[:success] == true
                  `killAll MavensMate`
                end
                result = {
                  :success => true
                }
                body = result.to_json
              rescue Exception => e
                result = {
                  :success  => false, 
                  :message  => e.message + "\n\n" + e.backtrace.join("\n")
                }
                body = result.to_json
              end 
              File.open("#{tmp_directory}/.response", 'w') {|f| f.write(body) }
            } 
            MavensMate::LocalServerThin.respond_with_async_request_id(request_id)
          end
        end

        #TODO: not async...does it need to be?
        class MetadataListServlet
          def call(env)            
            req = Rack::Request.new(env)
            begin              
              sid       = req["sid"]
              meta_type = req["key"]
              murl      = req["murl"]
              murl      = URI.unescape(murl)
              client = MavensMate::Client.new({ 
                :sid => sid, 
                :metadata_server_url => murl 
              })
              result = client.list(meta_type, false)
              
              body = result 
            rescue Exception => e
                result = {
                  :success => false, 
                  :message => e.message 
                }
                body = result
            end
            MavensMate::LocalServerThin.respond(body, 'text/plain')
          end    
        end
        
        #TODO: not async...does it need to be?
        class VersionControlServlet
          def call(env)            
            req = Rack::Request.new(env)
            begin              
              svn_un  = req["svn_un"]
              svn_pw  = req["svn_pw"]
              vc_type = req["vc_type"].downcase!
              vc_url  = req["vc_url"]
              
              require 'rubygems'
              require 'nokogiri'
              opts = []
              if vc_type == "svn"
                response = %x{svn list --xml --trust-server-cert --non-interactive --username #{svn_un} --password #{svn_pw} '#{vc_url}'}                    
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
              body = opts.to_json
            rescue Exception => e
              puts e.message
            end
            MavensMate::LocalServerThin.respond(body, 'text/json')
          end    
        end

        #used to immediately respond with the async request id 
        def respond_with_async_request_id(id)
          r = MavensMate::LocalServerThin.prepare_response({
            :status => "pending",
            :id     => id
          })
          MavensMate::LocalServerThin.respond(r, 'text/json')
        end

        def prepare_response(options={})
          result = {
            :status   => options[:status],
            :success  => options[:success] || "",
            :id       => options[:id]
          }
          return result.to_json
        end
        
      end
        
  end 
end