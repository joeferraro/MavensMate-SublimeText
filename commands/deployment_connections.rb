#!/usr/bin/env ruby -W0
require File.dirname(File.dirname(__FILE__)) + "/constants.rb"
include Constants
require SUPPORT + "/environment.rb"
require CONTROLLERS_ROOT + "/org_connection_controller.rb"
ENV["MM_CURRENT_PROJECT_DIRECTORY"] = ARGV[0]
dispatch :controller => "org_connection", :action => "index"
