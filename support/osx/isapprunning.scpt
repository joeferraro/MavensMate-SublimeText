if appIsRunning("TextMate") then
	set isRunning to true
else
	set isRunning to false
end if


on appIsRunning(appName)
	tell application "System Events" to (name of processes) contains appName
end appIsRunning