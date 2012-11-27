module Constants
	CLIENT_NAME = "MavensMate"
  ROOT = File.dirname(__FILE__)
  SUBLIME_PACKAGES_ROOT = File.dirname(ROOT)
  SUBLIME_USER_ROOT = SUBLIME_PACKAGES_ROOT + "/User"
	SUPPORT = ROOT + "/support"
	LIB_ROOT = SUPPORT + "/lib"
 	TMVC_ROOT = SUPPORT + "/tmvc"
 	CONTROLLERS_ROOT = SUPPORT + "/app/controllers"
 	HELPERS_ROOT = SUPPORT + "/app/helpers" 
	VIEWS_ROOT = SUPPORT + "/app/views"
	ENV["TM_BUNDLE_SUPPORT"] = SUPPORT
  ENV["CLIENT_NAME"] = CLIENT_NAME

  require 'rubygems'
  require 'json'
  begin
    MM_DEFAULT_CONFIG = JSON.parse(File.read("#{ROOT}/mavensmate.sublime-settings"))
    MM_USER_CONFIG = JSON.parse(File.read("#{SUBLIME_USER_ROOT}/mavensmate.sublime-settings"))
  rescue
    #TODO
  end

  MM_LOG_LEVEL  = MM_USER_CONFIG['mm_log_level'] || MM_DEFAULT_CONFIG['mm_log_level'] || 'FATAL'
  MM_SOAP_LOG   = MM_USER_CONFIG['mm_soap_log']  || MM_DEFAULT_CONFIG['mm_soap_log']  || false
  MM_WORKSPACE  = MM_USER_CONFIG['mm_workspace'] || MM_DEFAULT_CONFIG['mm_workspace'] || ''
end