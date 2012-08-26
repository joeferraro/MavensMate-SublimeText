# encoding: utf-8
require SUPPORT + '/lib/mavensmate.rb'

class ExecuteController < ApplicationController
    
  layout "base", :only => [:index]
            
  def index
    render "_index"
  end
  
end