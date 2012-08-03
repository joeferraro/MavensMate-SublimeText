#!/usr/bin/env ruby -W0
require File.dirname(File.dirname(__FILE__)) + "/constants.rb"
include Constants
ENV["MM_CURRENT_PROJECT_DIRECTORY"] = ARGV[0]
require LIB_ROOT + "/mavensmate.rb"
MavensMate.compile_project