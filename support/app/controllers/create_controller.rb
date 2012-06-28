# encoding: utf-8
require ENV['TM_BUNDLE_SUPPORT'] + '/lib/mavensmate.rb'
require ENV['TM_BUNDLE_SUPPORT'] + '/lib/metadata_helper.rb'

class CreateController < ApplicationController
  
  include MetadataHelper  
  
  layout "base"
          
  def index
    render "_create", :locals => {:meta_type => params[:meta_type], :meta_label => META_LABEL_MAP[params[:meta_type]],  :message => ""}
  end
  
  def create_metadata  
    #TODO - fix issue where failed deploy breaks form
    
    if params[:api_name].nil?
      TextMate::UI.alert(:warning, "MavensMate", "Please enter the API name")
      abort
    end
    if params[:api_name].include?(" ")
      TextMate::UI.alert(:warning, "MavensMate", "Your API name cannot contain spaces")
      abort
    end
    
    result = MavensMate.new_metadata({
      :meta_type => params[:meta_type], 
      :api_name => params[:api_name], 
      :object_api_name => params[:object_api_name],
      :apex_class_type => params[:apex_class_type]
    }) 
    result = MavensMate::Util.parse_deploy_response(result)
    render "_create_result", :locals => { :result => result }
  end
  
end