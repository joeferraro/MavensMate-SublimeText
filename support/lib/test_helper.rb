#!/usr/bin/env ruby -W0
MM_ROOT = File.dirname(__FILE__)
ENV['TM_BUNDLE_SUPPORT'] = MM_ROOT + "/.."
SUPPORT = ENV['TM_SUPPORT_PATH']
BUNDLESUPPORT = ENV['TM_BUNDLE_SUPPORT']
require BUNDLESUPPORT + '/lib/mavensmate'
require SUPPORT + '/lib/exit_codes'
require SUPPORT + '/lib/escape'
require SUPPORT + '/lib/textmate'
require SUPPORT + '/lib/ui'
require SUPPORT + '/lib/web_preview'
require SUPPORT + '/lib/progress'
require 'rexml/document'
require 'fileutils'
require BUNDLESUPPORT + '/lib/client'
require BUNDLESUPPORT + '/lib/factory'
require BUNDLESUPPORT + '/lib/exceptions'
require BUNDLESUPPORT + '/lib/metadata_helper'
require BUNDLESUPPORT + '/lib/util'
require ENV['TM_SUPPORT_PATH'] + '/lib/ui'
require ENV['TM_SUPPORT_PATH'] + '/lib/current_word'
require 'yaml' 
require 'rubygems'
require 'diffy' 

module TestHelper
   
  class << self
    
     def login(un, pw, env)
        endpoint = (env == "test") ? "https://test.salesforce.com/services/Soap/u/24.0" : "https://www.salesforce.com/services/Soap/u/24.0"    
        client = MavensMate::Client.new({ :username => un, :password => pw, :endpoint => endpoint })
     end
  
  end

end
