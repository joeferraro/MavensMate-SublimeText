# encoding: utf-8
require ENV['TM_BUNDLE_SUPPORT'] + '/lib/mavensmate.rb'
require ENV['TM_BUNDLE_SUPPORT'] + '/lib/factory.rb'
require ENV['TM_BUNDLE_SUPPORT'] + '/lib/metadata_helper.rb'
require ENV['TM_BUNDLE_SUPPORT'] + '/lib/object.rb'
require ENV['TM_BUNDLE_SUPPORT'] + '/lib/util.rb'
class OrgConnectionController < ApplicationController
  
  include MetadataHelper  
  
  layout "base", :only => [:index, :new_connection, :delete_connection]
          
  def index        
    render "_index", :locals => { :connections => get_connections }
  end
  
  #adds a new deployment connection to a project, stores creds in keychain
  def new_connection
    begin
      un = params[:un].to_s
      pw = params[:pw].to_s
      server_url = params[:server_url].to_s
      
      TextMate.call_with_progress( :title => "MavensMate", :message => "Validating Salesforce.com Credentials" ) do
        client = MavensMate::Client.new({ :username => params[:un], :password => params[:pw], :endpoint => params[:server_url] })
      end
            
      environment = (server_url.include? "test") ? "sandbox" : "production"
      require 'yaml'
      yml = YAML::load(File.open("#{ENV['TM_PROJECT_DIRECTORY']}/config/settings.yaml")) 
      project_name = yml['project_name']      
      if yml["org_connections"]
        connections = yml["org_connections"]
        keychain_name = project_name + "-mm-"
        %x{security add-generic-password -a '#{project_name}-mm-#{un}' -s \"#{project_name}-mm-#{un}\" -w #{pw} -U}         
        connections.push({ "username" => un, "environment" => environment })
      else
        %x{security add-generic-password -a '#{project_name}-mm-#{un}' -s \"#{project_name}-mm-#{un}\" -w #{pw} -U} 
        yml["org_connections"] = [{ "username" => un, "environment" => environment }]
      end 
      File.open("#{ENV['TM_PROJECT_DIRECTORY']}/config/settings.yaml", 'w') { |f| YAML.dump(yml, f) }
          
      render "_index", :locals => { :connections => get_connections }
    rescue Exception => e
      TextMate::UI.alert(:warning, "MavensMate", e.message)  
      render "_index", :locals => { :connections => get_connections }
    end
  end
  
  #removes a deployment connection from a project
  def delete_connection
    begin
      un = params[:un]
      require 'yaml'
      yml = YAML::load(File.open("#{ENV['TM_PROJECT_DIRECTORY']}/config/settings.yaml")) 
      project_name = yml['project_name']      
      if yml["org_connections"]
        conns = yml["org_connections"]
        conns.delete_if{|conn| conn["username"] == un }
        yml["org_connections"] = conns
      end
      File.open("#{ENV['TM_PROJECT_DIRECTORY']}/config/settings.yaml", 'w') { |f| YAML.dump(yml, f) }      
      render "_index", :locals => { :connections => get_connections }
    rescue Exception => e
      TextMate::UI.alert(:warning, "MavensMate", e.message + "\n" + e.backtrace.join("\n"))  
    end
  end
  
  #retrieves list of deployment connections from this project
  def get_connections
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
   
end