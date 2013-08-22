#MavensMate for Sublime Text

MavensMate for Sublime Text is a plugin that aims to replicate the functionality of the Eclipse-based Force.com IDE. Its goal is to allow developers to work inside Sublime Text for all their Force.com-related tasks.

* Create & Edit Salesforce.com projects with specific package metadata
* Create & compile Apex Classes, Apex Trigger, Visualforce Pages, and Visualforce Components
* Compile and retrieve other Salesforce.com metadata
* Run Apex test methods and visualize test successes/failures & coverage
* Play Pacman, Tetris, and Donkey Kong while your Apex unit tests and deploys run
* Deploy metadata to other Salesforce.com orgs
* Apex Execute Anonymous
* Create Apex Execution Overlay Actions "checkpoints" (tooling API)
* Download Apex Logs (tooling API)
* Apex & Visualforce Code Assist

####For detailed information and documentation, please visit [mavensmate.com][mmcom]


##Sublime Text 3 plugin (current stable version)

###Prerequisites

####Mac OSX (OSX 10.7+ only)
You must have MavensMate.app installed. Download MavensMate.app [here][mm_download] and place in /Applications

###Install

####Mac OSX (OSX 10.7+ only)
To install the Sublime Text 3 Plugin for MavensMate, go to the "Plugins" menu in MavensMate.app and install the plugin.

<img src="http://wearemavens.com/images/mm/plugins-menu.png" width="300"/>

<img src="http://wearemavens.com/images/mm/plugins.png" width="400"/>

####Windows
TODO

####Linux
You must have Python 2.7 installed (you can likely use system python)

```
easy_install jinja2 suds keyring markupsafe pyyaml requests
```

OR

```
pip install jinja2 suds keyring markupsafe pyyaml requests

```


##Sublime Text 2 plugin (no longer supported)

###Prerequisites

####Mac OSX (OSX 10.7+ only)
You must have **MavensMate.app 0.34** installed. Download [MavensMate.app v0.34][mm_034_download] and place in /Applications

##Install
To install the Sublime Text 2 Plugin for MavensMate, go to the "Plugins" menu in MavensMate.app and install the plugin.

<img src="http://wearemavens.com/images/mm/plugins-menu.png" width="300"/>

<img src="http://wearemavens.com/images/mm/plugins.png" width="400"/>


##Setup
<img src="http://wearemavens.com/images/mm/menu3.png" width="400"/>

Go to `MavensMate > Settings > User` and modify `mm_workspace` with the EXISTING location where you'd like your MavensMate projects to reside, for example (notice the absolute path):

	"mm_workspace": "/Users/your_username/Projects"

##Update

###Mac OSX (OSX 10.7+ only)
If `mm_check_for_updates` is set to `true`, MavensMate will check for updates when Sublime Text starts up. If an update is available, you can update the plugin through the "Plugins" panel in MavensMate.app.

<img src="http://wearemavens.com/images/mm/plugin-update.png" width="400"/>

###Windows
TODO

###Linux
If `mm_check_for_updates` is set to `true`, MavensMate will check for updates when Sublime Text starts up. If an update is available...

##Documentation
<a href="MavensMate Documentation">http://mavensmate.com/Getting_Started/Developers</a>

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

[mm_download]: http://cdn.mavensconsulting.com/mavensmate/builds/MavensMate.zip
[mm_034_download]: http://cdn.mavensconsulting.com/mavensmate/builds/0.34/MavensMate.zip
[mmcom]: http://mavensmate.com/?utm_source=github&utm_medium=st-plugin&utm_campaign=st
