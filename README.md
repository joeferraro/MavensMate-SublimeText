#MavensMate

MavensMate is a SublimeText plugin that aims to replicate the functionality of the Eclipse-based Force.com IDE.

* Create & Edit Salesforce.com projects with specific package metadata
* SVN & Git support
* Create & compile Apex Classes, Apex Trigger, Visualforce Pages, and Visualforce Components
* Compile and retrieve other Salesforce.com metadata
 
##Clean Install
```
$ gem install mavensmate
```

```
$ cd ~/Library/Application\ Support/Sublime\ Text\ 2/Packages
$ git clone git://github.com/joeferraro/MavensMate-SublimeText.git "MavensMate"
```

Open Sublime Text, go to Preferences (command + ,) and add a declaration for where you'd like your MavensMate projects to reside, for example (notice the absolute path):

	"mm_workspace": "/Users/your_username/Projects"

##Update

```
$ cd ~/Library/Application\ Support/Sublime\ Text\ 2/Packages
$ rm -rf ~/Library/Application\ Support/Sublime\ Text\ 2/Packages/MavensMate
$ git clone git://github.com/joeferraro/MavensMate-SublimeText.git "MavensMate"
```

##Screenshots

###Project Wizard
<img src="http://wearemavens.com/images/mm/project_wizard.png"/>