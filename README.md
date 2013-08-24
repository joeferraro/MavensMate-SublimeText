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

###Install

####Mac OSX (OSX 10.7+ only)
1. You must have MavensMate.app installed. Download MavensMate.app [here][mm_download] and place in /Applications
2. To install the Sublime Text 3 Plugin for MavensMate, go to the "Plugins" menu in MavensMate.app and install the plugin.

<img src="http://wearemavens.com/images/mm/plugins-menu.png" width="300"/>

<img src="http://wearemavens.com/images/mm/plugins.png" width="400"/>

####Linux
1. You must have python 2.7 and git installed
2. Install required modules `$ easy_install jinja2 suds keyring markupsafe pyyaml requests`
3. Run install script `$ python < <(curl -s https://raw.github.com/joeferraro/MavensMate-SublimeText/dev/install-dev.py)`
4. Alias your `subl` command line tool to `/usr/local/bin`

```
$ cd /usr/local/bin
$ sudo ln -s /usr/bin/subl subl
```

####Windows
1. You must have python 2.7 and git installed
2. Install required modules `easy_install jinja2 suds keyring markupsafe pyyaml requests`
3. Close Sublime Text
4. Download and run python install script: `https://raw.github.com/joeferraro/MavensMate-SublimeText/dev/install-dev.py`



##Sublime Text 2 plugin (no longer supported)

###Prerequisites

####Mac OSX (OSX 10.7+ only)
You must have **MavensMate.app 0.34** installed. Download [MavensMate.app v0.34][mm_034_download] and place in /Applications

###Install
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

###Linux
NOT SUPPORTED

###Windows
NOT SUPPORTED

##Documentation
<a href="MavensMate for Sublime Text Documentation">http://mavensmate.com/Plugins/Sublime_Text/Overview</a>

##Screenshots

###Project Wizard
<img src="http://cdn.mavensconsulting.com/mavensmate/img/new-project.png"/>
###Apex Test Runner
<img src="http://cdn.mavensconsulting.com/mavensmate/img/tests.png"/>
###Apex Execute Anonymous
<img src="http://cdn.mavensconsulting.com/mavensmate/img/execute-apex.png"/>
###Quick Panel
<img src="http://wearemavens.com/images/mm/panel.png"/>
###Apex/Visualforce Code Assist
<img src="http://cdn.mavensconsulting.com/mavensmate/img/apex2.png"/>
<img src="http://cdn.mavensconsulting.com/mavensmate/img/vf1.png"/>
<img src="http://cdn.mavensconsulting.com/mavensmate/img/vf2.png"/>

[mm_download]: http://cdn.mavensconsulting.com/mavensmate/builds/MavensMate.zip
[mm_034_download]: http://cdn.mavensconsulting.com/mavensmate/builds/0.34/MavensMate.zip
[mmcom]: http://mavensmate.com/?utm_source=github&utm_medium=st-plugin&utm_campaign=st
