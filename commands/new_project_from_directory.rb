#!/usr/bin/env ruby -W0
require File.dirname(File.dirname(__FILE__)) + "/constants.rb"
include Constants
require SUPPORT + "/environment.rb"
require CONTROLLERS_ROOT + "/project_controller.rb"
ENV["MM_CURRENT_PROJECT_DIRECTORY"] = ARGV[0]
ENV["MM_WORKSPACE"] = ARGV[1]
dispatch :controller => "project", :action => "index_new_from_existing", :user_action => "new"
