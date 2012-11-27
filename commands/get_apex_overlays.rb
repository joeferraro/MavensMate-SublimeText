#!/usr/bin/env ruby -W0
require File.dirname(File.dirname(__FILE__)) + "/constants.rb"
include Constants
ENV["MM_CURRENT_PROJECT_DIRECTORY"] = ""#??
ENV["TM_FILEPATH"] = ARGV[0]
require LIB_ROOT + "/client.rb"
MavensMate::Util.set_project_directory(File.dirname(ENV["TM_FILEPATH"]))
client = MavensMate::Client.new
apex_entity_id = client.get_apex_entity_id_by_name({:file_name => ENV["TM_FILEPATH"]})
overlays = client.list_execution_overlays({:id => apex_entity_id})
puts overlays.to_json