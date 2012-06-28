on run argv
    set eventDescription to (item 1 of argv)

	tell application "System Events"
		set isRunning to (count of (every process whose bundle identifier is "com.Growl.GrowlHelperApp")) > 0
	end tell

	if isRunning then
		tell application id "com.Growl.GrowlHelperApp"
		
			-- Make a list of all the notification types 
			-- that this script will ever send:
			set the allNotificationsList to ¬
				{"MavensMate"}
		
			-- Make a list of the notifications 
			-- that will be enabled by default.      
			-- Those not enabled by default can be enabled later 
			-- in the 'Applications' tab of the growl prefpane.
			set the enabledNotificationsList to ¬
				{"MavensMate"}
		
			-- Register our script with growl.
			-- You can optionally (as here) set a default icon 
			-- for this script's notifications.
			register as application ¬
				"MavensMate" all notifications allNotificationsList ¬
				default notifications enabledNotificationsList ¬
				icon of application "TextMate"
			
			notify with name ¬
				"MavensMate" title ¬
				"MavensMate" description ¬
				eventDescription application name "MavensMate"
				
		end tell
	end if  

end run      
