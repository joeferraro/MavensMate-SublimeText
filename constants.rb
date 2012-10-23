module Constants
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
end