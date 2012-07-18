#MavensMate

MavensMate is a SublimeText plugin that aims to replicate the functionality of the Eclipse-based Force.com IDE.

* Create & Edit Salesforce.com projects with specific package metadata
* SVN & Git support
* Create & compile Apex Classes, Apex Trigger, Visualforce Pages, and Visualforce Components
* Compile and retrieve other Salesforce.com metadata
* Run Apex test methods and visualize test successes/failures & coverage

*Currently, MavensMate only officially supports OS X. It's on the roadmap to fully support Windows/Linux.
 
##Install
```
$ gem install mavensmate
$ ruby < <(curl -s https://raw.github.com/joeferraro/MavensMate-SublimeText/master/install.rb)
```

Open Sublime Text, go to Preferences (command + ,) and add a declaration for where you'd like your MavensMate projects to reside, for example (notice the absolute path):

	"mm_workspace": "/Users/your_username/Projects"

So, your Preferences.sublime-settings file may look something like this:

	{
		"color_scheme": "Packages/User/Espresso Soda.tmTheme",
		"font_size": 17,
		"mm_workspace": "/Users/your_username/Projects",
		"mm_api_version": "25.0"
	}


###RVM
If you're using RVM and you want Sublime Text to use your RVM ruby, you will likely need to modify Sublime Text's ruby settings file:
````
~/Library/Application\ Support/Sublime\ Text\ 2/Packages/Ruby/Ruby.sublime-build
````

Modify it to look like this:
	
	{
		"cmd": ["/Users/your_username_here/.rvm/bin/rvm-auto-ruby", "$file"],
		"file_regex": "^(...*?):([0-9]*):?([0-9]*)",
		"selector": "source.ruby"
	}


##Update

```
$ ruby < <(curl -s https://raw.github.com/joeferraro/MavensMate-SublimeText/master/install.rb)
```

##Screenshots

###Project Wizard
<img src="http://wearemavens.com/images/mm/project_wizard.png"/>
###Apex Test Runner
<img src="http://wearemavens.com/images/mm/test2.png"/>