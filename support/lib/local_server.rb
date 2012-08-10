# encoding: utf-8
require 'rubygems'
require 'json'
require File.dirname(File.dirname(File.dirname(__FILE__))) + "/constants.rb"
include Constants
require File.dirname(__FILE__) + '/lsof.rb'
require File.dirname(__FILE__) + '/mavensmate.rb'
require 'webrick'
include WEBrick

module MavensMate
  module LocalServer
            
      class << self
        
        def start_test
          server = WEBrick::HTTPServer.new(:Port => 7777)
          ['INT', 'TERM'].each { |signal|
             trap(signal) { server.shutdown } 
          }
          
          server.mount('/project', ProjectServlet)
          server.mount('/metadata/list', MetadataListServlet) 
          server.mount('/vc', VersionControlServlet) 
          server.mount('/auth', AuthenticationServlet)
          server.mount('/test', ApexUnitTestServlet)
          server.mount('/metadata/index', MetadataIndexServlet)
          server.mount('/deploy', DeployServlet)
          server.start  
        end

        def start
          stop
          exit if fork            # Parent exits, child continues.
          Process.setsid          # Become session leader.
          exit if fork            # Zap session leader.
          
          pid = fork do
            server = WEBrick::HTTPServer.new(:Port => 7777)
            
            ['INT', 'TERM'].each { |signal|
               trap(signal) { server.shutdown } 
            }
            
            server.mount('/project', ProjectServlet)
            server.mount('/metadata/list', MetadataListServlet) 
            server.mount('/vc', VersionControlServlet) 
            server.mount('/auth', AuthenticationServlet)
            server.mount('/test', ApexUnitTestServlet)
            server.mount('/metadata/index', MetadataIndexServlet)
            server.mount('/deploy', DeployServlet)
            server.start  
          end   
          Process.detach(pid)
        end
      
        def stop
          if Lsof.running?(7125)
            Lsof.kill(7125)
          end
          if Lsof.running?(7777)
            Lsof.kill(7777)
          end          
        end

        class ApexUnitTestServlet < WEBrick::HTTPServlet::AbstractServlet
          def do_POST(req, resp)
            ENV["MM_CURRENT_PROJECT_DIRECTORY"] = req.query["mm_current_project_directory"]
            require SUPPORT + "/environment.rb"
            require File.dirname(File.dirname(File.dirname(__FILE__))) + "/support/tmvc/lib/application_controller.rb"
            resp['Content-Type'] = 'html'
            test_result = {}
            begin
              result = MavensMate.run_tests(req.query["selected_tests"].split(","))
              ac = ApplicationController.new
              if RUBY_VERSION =~ /1.9/
                Encoding.default_external = Encoding::UTF_8
                Encoding.default_internal = Encoding::UTF_8
              end 
              html = ac.render_to_string "unit_test/_test_result", :locals => { :result => result }
              resp.body = html
            rescue Exception => e
              #puts e.message + "\n\n" + e.backtrace.join("\n")
              #resp.body = "TEST RESULT: " + test_result.inspect + "\n\n" + "Request: " + req.inspect + "\n\n" + e.message + "\n\n" + e.backtrace.join("\n")
              result = {
                  :success  => false, 
                  :message  => e.message + e.backtrace.join("\n") 
              }
              resp.body = result.to_json
            end
          end
        end

        #indexes server metadata to the .org_metadata file in the project config folder
        class MetadataIndexServlet < WEBrick::HTTPServlet::AbstractServlet
          def do_GET(req, resp)            
            begin              
              resp['Content-Type'] = 'html'
              ENV["MM_CURRENT_PROJECT_DIRECTORY"] = req.query["mm_current_project_directory"]
              do_refresh = req.query["do_refresh"]
              metadata_array = nil
              if do_refresh == "true" or do_refresh == true
                metadata_array = MavensMate.build_index
              else
                metadata_array = eval(File.read("#{ENV['MM_CURRENT_PROJECT_DIRECTORY']}/config/.org_metadata")) #=> comprehensive list of server metadata    
              end
              ac = ApplicationController.new
              html = ac.render_to_string "deploy/_metadata_tree", :locals => { :meta_array => metadata_array }
              resp.body = html
            rescue Exception => e
                resp['Content-Type'] = 'json'
                result = {
                  :success  => false, 
                  :message  => e.message + "\n\n" + e.backtrace.join("\n")
                }
                resp.body = result.to_json
            end
          end    
        end

        class DeployServlet < WEBrick::HTTPServlet::AbstractServlet
          def do_POST(req, resp)    
            begin
              resp['Content-Type'] = 'html'
              ENV["MM_CURRENT_PROJECT_DIRECTORY"] = req.query["mm_current_project_directory"]
              params = {}
              params[:un]           = req.query["un"]
              params[:pw]           = req.query["pw"]
              params[:server_url]   = req.query["server_url"]
              params[:package]      = eval(req.query["tree"])
              params[:check_only]   = req.query["check_only"]
              params[:package_type] = "Custom"
              deploy_result = MavensMate.deploy_to_server(params)
              html = nil
              begin
                result = MavensMate::Util.parse_deploy_response(deploy_result)
                ac = ApplicationController.new
                html = ac.render_to_string "deploy/_deploy_result", :locals => { :result => result, :is_check_only => params[:check_only] }
              rescue
                html = '<div id="error_message" class="alert-message error"><p><strong>Deployment Failed!</strong></p><p>'+deploy_result[:message]+'</p></div> '
              end
              resp.body = html
            rescue Exception => e
              result = '<div id="error_message" class="alert-message error"><p><strong>Deployment Failed!</strong></p><p>'+e.message+'</p></div> '
              resp.body = result
            end
          end
        end

        
        class ProjectServlet < WEBrick::HTTPServlet::AbstractServlet
          def do_POST(req, resp)            
            begin
              params = {}
              params[:action]     = req.query["action"]
              params[:pn]         = req.query["pn"]
              params[:un]         = req.query["un"]
              params[:pw]         = req.query["pw"]
              params[:server_url] = req.query["server_url"]
              params[:vc_un]      = req.query["vc_un"]
              params[:vc_pw]      = req.query["vc_pw"]
              params[:vc_url]     = req.query["vc_url"]
              params[:vc_type]    = req.query["vc_type"]
              params[:vc_alias]   = req.query["vc_alias"]
              params[:vc_branch]  = req.query["vc_branch"]
              params[:package]    = eval(req.query["tree"]) if params[:action] == "new"
              params[:where]      = req.query["where"] 
              ENV["MM_WORKSPACE"] = req.query["where"]
              if params[:action] == "checkout"
                result = MavensMate.checkout_project(params)
              else
                result = MavensMate.new_project(params)
              end           
              if result[:success]
                `killAll MavensMate` 
                #`~/bin/subl --project '#{ENV["MM_WORKSPACE"]}/#{params[:pn]}/.sublime-project'` if result[:success]
                `'/Applications/Sublime Text 2.app/Contents/SharedSupport/bin/subl' --project '#{ENV["MM_WORKSPACE"]}/#{params[:pn]}/.sublime-project'` if result[:success]
              else
                resp.body = result.to_json
              end
            rescue Exception => e
              puts e.message
              resp.body = e.message.to_json
            end
          end
        end
            
        class MetadataNewServlet < WEBrick::HTTPServlet::AbstractServlet
          def do_POST(req, resp)            
            begin              
              result = MavensMate.new_metadata({
                :meta_type        => req.query["meta_type"], 
                :api_name         => req.query["api_name"], 
                :object_api_name  => req.query["object_api_name"],
                :apex_class_type  => req.query["apex_class_type"]
              }) 
              puts result.inspect
              `killAll MavensMate` if result[:success] #=> result[:message] 
              #`~/bin/subl --command '#{ENV["MM_CURRENT_PROJECT_DIRECTORY"]}/#{params[:pn]}/.sublime-project'` if result[:success]
              `/Applications/Sublime\ Text\ 2.app/Contents/SharedSupport/bin/subl --command '#{ENV["MM_CURRENT_PROJECT_DIRECTORY"]}/#{params[:pn]}/.sublime-project'` if result[:success]
              #windows it's sublime_text --command
            rescue Exception => e
              puts e.message
            end
          end    
        end

        class AuthenticationServlet < WEBrick::HTTPServlet::AbstractServlet
          def do_GET(req, resp)            
            begin              
              sid = nil
              murl = nil
              client = MavensMate::Client.new({ 
                :username => req.query["un"], 
                :password => req.query["pw"], 
                :endpoint => req.query["server_url"] 
              })
              if ! client.sid.nil? && ! client.metadata_server_url.nil?
                result = {
                  :success  => true, 
                  :sid      => client.sid, 
                  :murl     => client.metadata_server_url 
                }
                resp.body = result.to_json
              end
            rescue Exception => e
                result = {
                  :success  => false, 
                  :message  => e.message 
                }
                resp.body = result.to_json
            end
          end    
        end

        class MetadataListServlet < WEBrick::HTTPServlet::AbstractServlet
          def do_GET(req, resp)            
            begin              
              sid       = req.query["sid"]
              meta_type = req.query["key"]
              murl      = req.query["murl"]
              murl      = URI.unescape(murl)
              client = MavensMate::Client.new({ 
                :sid => sid, 
                :metadata_server_url => murl 
              })
              result = client.list(meta_type, false)
              resp.body = result 
            rescue Exception => e
                result = {
                  :success => false, 
                  :message => e.message 
                }
                resp.body = result
            end
          end    
        end
        
        class VersionControlServlet < WEBrick::HTTPServlet::AbstractServlet
          def do_GET(req, resp)            
            begin              
              svn_un  = req.query["svn_un"]
              svn_pw  = req.query["svn_pw"]
              vc_type = req.query["vc_type"].downcase!
              vc_url  = req.query["vc_url"]
              
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
              resp.body = opts.to_json
            rescue Exception => e
              puts e.message
            end
          end    
        end
        
      end
        
  end 
end