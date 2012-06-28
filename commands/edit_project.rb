#!/usr/bin/env ruby -W0
require "rubygems"
require "savon"
require "builder"
require "zip/zipfilesystem"
require File.dirname(File.dirname(__FILE__)) + "/constants.rb"
include Constants
require SUPPORT + "/environment.rb"
require CONTROLLERS_ROOT + "/project_controller.rb"
dispatch :controller => "project", :action => "index_edit", :user_action => "edit"
