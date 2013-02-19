#!/usr/bin/env ruby -W0
require File.dirname(File.dirname(__FILE__)) + "/constants.rb"
include Constants
ENV["MM_CURRENT_PROJECT_DIRECTORY"] = ARGV[1]
file = File.open(ARGV[0], "rb")
file_string = file.read
ENV["TM_SELECTED_FILES"] = file_string
require LIB_ROOT + "/mavensmate.rb"
MavensMate.compile_selected_files