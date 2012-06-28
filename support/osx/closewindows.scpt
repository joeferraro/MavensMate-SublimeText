set closedCount to 0
tell application "System Events"
  
  if not UI elements enabled then
    try
      tell application "TextMate" to set answer to button returned of (display dialog "The command that closes MavensMate dialogs after form submission relies on the GUI scripting architecture of Mac OS X which is currently disabled." & return & return & "You can activate it by selecting the checkbox \"Enable access for assistive devices\" in the Universal Access preference pane. Otherwise, you'll need to close MavensMate dialog windows manually. Thanks!" buttons {"OK"} default button 1 with icon 1)
    on error number -128
      -- User cancelled
    end try
    return
  end if
  
  tell process "TextMate"
    repeat with i from (count windows) to 1 by -1 -- iterate backwards so indices don't shift on close
      try
        tell the first UI element of the first scroll area of window i
          if role is "AxWebArea" then
            tell application "TextMate" to close window i
            set closedCount to closedCount + 1
          end if
        end tell
      end try
    end repeat
  end tell

end tell

-- FIXME: This count is sometimes the expected value + 1 -- why?
if closedCount is 0
  return "No HTML output windows to close."
else if closedCount is 1
  return "Closed 1 HTML output window."
else 
  return "Closed "&closedCount&" HTML output windows."
end if