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
  
  layout "base", :only => [:index_new, :index_edit, :index_new_from_existing]

  def index_new
    my_json = File.read("#{ENV['TM_BUNDLE_SUPPORT']}/conf/metadata_describe.json")
    support_folder = ENV['TM_BUNDLE_SUPPORT']
    sf = support_folder.gsub(/lib\/../, "")
    render "_project_new", :locals => { :user_action => params[:user_action], :my_json => my_json, :child_metadata_definition => CHILD_META_DICTIONARY, :support_folder => sf}
  end 
   
  def index_edit
    pconfig = MavensMate.get_project_config
    password = KeyChain::find_internet_password("#{pconfig['project_name']}-mm")
    render "_project_edit", :locals => { 
      :child_metadata_definition => CHILD_META_DICTIONARY, 
      :pname => pconfig['project_name'], 
      :pun => pconfig['username'], 
      :ppw => password, 
      :pserver_url => MavensMate::Util.get_short_sfdc_endpoint_by_type(pconfig['environment'])
    }
  end

  def index_new_from_existing
    support_folder = ENV['TM_BUNDLE_SUPPORT']
    pname = ENV["MM_CURRENT_PROJECT_DIRECTORY"].split("/").last
    sf = support_folder.gsub(/lib\/../, "")
    render "_project_new_from_existing", :locals => { :pname => pname, :user_action => "new_from_existing_directory", :support_folder => sf, :existing_directory => "#{ENV["MM_CURRENT_PROJECT_DIRECTORY"]}"}
  end     
end