#!/usr/bin/env ruby -W0
require File.dirname(File.dirname(__FILE__)) + "/constants.rb"
include Constants
ENV["TM_FILEPATH"] = ARGV[0]
require LIB_ROOT + "/mavensmate.rb"
MavensMate::Util.set_project_directory(File.dirname(ENV["TM_FILEPATH"]))
MavensMate.refresh_selected_file