#!/usr/bin/env ruby -W0
require File.dirname(File.dirname(__FILE__)) + "/constants.rb"
require 'json'
include Constants
require LIB_ROOT + "/mavensmate.rb"
# :meta_type => req.query["meta_type"], 
# :api_name => req.query["api_name"], 
# :object_api_name => req.query["object_api_name"],
# :apex_class_type => req.query["apex_class_type"]
ENV["MM_CURRENT_PROJECT_DIRECTORY"] = ARGV[1]
params = JSON.parse(ARGV[0], :symbolize_names => true)
MavensMate.new_metadata(params)