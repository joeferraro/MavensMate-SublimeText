#!/usr/bin/env ruby -W0
require File.dirname(File.dirname(__FILE__)) + "/constants.rb"
include Constants
ENV["MM_CURRENT_PROJECT_DIRECTORY"] = ARGV[1]
tmp_file = File.open(ARGV[0], "rb")
dirs = tmp_file.read
require LIB_ROOT + "/mavensmate.rb"
MavensMate.clean_dirs({:dirs => dirs})