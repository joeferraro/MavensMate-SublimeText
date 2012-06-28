module Constants
	ROOT = File.dirname(__FILE__)
	SUPPORT = ROOT + "/support"
	LIB_ROOT = SUPPORT + "/lib"
 	TMVC_ROOT = SUPPORT + "/tmvc"
 	CONTROLLERS_ROOT = SUPPORT + "/app/controllers"
 	HELPERS_ROOT = SUPPORT + "/app/helpers" 
	VIEWS_ROOT = SUPPORT + "/app/views"
	ENV["TM_BUNDLE_SUPPORT"] = SUPPORT
	ENV["MM_WORKSPACE"] = ARGV[0] || ""
	ENV["MM_CURRENT_PROJECT_DIRECTORY"] = ""
end