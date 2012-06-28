#!/usr/bin/env ruby -W0
require File.dirname(File.dirname(__FILE__)) + "/constants.rb"
include Constants
ENV["MM_CURRENT_PROJECT_DIRECTORY"] = ARGV[0]
#ENV["TM_PROJECT_DIRECTORY"] = "/Users/josephferraro/Development/st/roooo"
require LIB_ROOT + "/mavensmate.rb"
MavensMate.clean_project({:update_sobjects => true})