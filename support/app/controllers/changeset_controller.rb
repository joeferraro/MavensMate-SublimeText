# encoding: utf-8
require ENV['TM_BUNDLE_SUPPORT'] + '/lib/mavensmate.rb'
require ENV['TM_BUNDLE_SUPPORT'] + '/lib/factory.rb' 
require ENV['TM_BUNDLE_SUPPORT'] + '/lib/object.rb'
#require ENV['TM_BUNDLE_SUPPORT'] + '/app/controllers/project_controller.rb'

class ChangesetController < ApplicationController
  
  include MetadataHelper
    
  layout "base", :only => [:index]
  
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
    
    MavensMate.build_index if confirmed
    project_array = eval(File.read("#{ENV['TM_PROJECT_DIRECTORY']}/config/.org_metadata")) #=> comprehensive list of server metadata
    
    render "_changeset_new", :locals => { :project_array => project_array, :child_metadata_definition => CHILD_META_DICTIONARY } 
  end
  
  def create
    begin
      tree = eval(params[:tree])  
      result = MavensMate.new_changeset({ :name => params[:name], :package => tree })
      render "_changeset_new_result", :locals => { :message => result[:message], :success => result[:success] }
    rescue Exception => e
      TextMate::UI.alert(:warning, "MavensMate", e.message)
    end
  end

end