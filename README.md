#MavensMate for Sublime Text plugin (2.0 beta)

MavensMate for Sublime Text is a plugin that aims to replicate the functionality of the Eclipse-based Force.com IDE. Its goal is to allow developers to work inside Sublime Text for all their Force.com-related tasks.

* Create & Edit Salesforce.com projects with specific package metadata
* Create & compile Apex Classes, Apex Trigger, Visualforce Pages, and Visualforce Components
* Compile and retrieve other Salesforce.com metadata
* Run Apex test methods and visualize test successes/failures & coverage
* Play Pacman, Tetris, and Donkey Kong while your Apex unit tests and deploys run
* Deploy metadata to other Salesforce.com orgs
* Apex Execute Anonymous
* Create Apex Execution Overlay Actions (tooling API)
* Download Apex Logs (tooling API)
* Apex Code Assist (beta!!)

##Prerequisites

###Mac OSX (OSX 10.7+ only)
You must have MavensMate.app installed. Download MavensMate.app [here][mm_download] and place in /Applications

###Windows
TODO: We're looking for talented Windows developers to own MavensMate for Windows. Please visit the MavensMate project on GitHub for more information: https://github.com/joeferraro/MavensMate

###Linux
TODO: We're looking for talented Linux developers to own MavensMate for Linux. Please visit the MavensMate project on GitHub for more information: https://github.com/joeferraro/MavensMate

##Install

To install the Sublime Text Plugin for MavensMate, go to the "Plugins" menu in MavensMate.app and install the plugin.

<img src="http://wearemavens.com/images/mm/plugins-menu.png" width="300"/>
 
<img src="http://wearemavens.com/images/mm/plugins.png" width="400"/>


##Setup
<img src="http://wearemavens.com/images/mm/menu3.png" width="400"/>

Go to "MavensMate --> Settings --> User" and modify `mm_workspace` with the EXISTING location where you'd like your MavensMate projects to reside, for example (notice the absolute path):

	"mm_workspace": "/Users/your_username/Projects"

##Update
If `mm_check_for_updates` is set to `true`, MavensMate will check for updates when Sublime Text starts up. If an update is available, you can update the plugin through the "Plugins" panel in MavensMate.app.

<img src="http://wearemavens.com/images/mm/plugin-update.png" width="400"/>

##Wiki
<a href="https://github.com/joeferraro/MavensMate-SublimeText/wiki">https://github.com/joeferraro/MavensMate-SublimeText/wiki</a>

##Screenshots

###Project Wizard
<img src="http://wearemavens.com/images/mm/project_wizard.png"/>
###Apex Test Runner
<img src="http://wearemavens.com/images/mm/test2.png"/>
###Apex Execute Anonymous
<img src="http://wearemavens.com/images/mm/execute.png"/>
###Quick Panel
<img src="http://wearemavens.com/images/mm/panel.png"/>
###Apex Code Assist
<img src="http://wearemavens.com/images/mm/code_3.png"/>
<img src="http://wearemavens.com/images/mm/code_4.png"/>
###Pacman
<img src="http://wearemavens.com/images/mm/pacman.png"/>

[mm_download]: http://joe-ferraro.com/mavensmate/MavensMate.zip
