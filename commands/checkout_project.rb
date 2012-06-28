#!/usr/bin/env ruby
# require "rubygems"
# require "savon"
# require "builder"
# require "zip/zipfilesystem"
require File.dirname(File.dirname(__FILE__)) + "/constants.rb"
include Constants
require SUPPORT + "/environment.rb"
require CONTROLLERS_ROOT + "/project_controller.rb"
ENV["MM_WORKSPACE"] = ARGV[0]
dispatch :controller => "project", :action => "index_new", :user_action => "checkout"
