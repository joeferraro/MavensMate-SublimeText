#MavensMate

MavensMate is a SublimeText plugin that aims to replicate the functionality of the Eclipse-based Force.com IDE.

* Create & Edit Salesforce.com projects with specific package metadata
* SVN & Git support
* Create & compile Apex Classes, Apex Trigger, Visualforce Pages, and Visualforce Components
* Compile and retrieve other Salesforce.com metadata
* Run Apex test methods and visualize test successes/failures & coverage
* Deploy metadata to other Salesforce.com orgs

*Currently, MavensMate only officially supports OS X. It's on the roadmap to fully support Windows/Linux.
 
##Install
```
$ gem install mavensmate
$ ruby < <(curl -s https://raw.github.com/joeferraro/MavensMate-SublimeText/master/install.rb)
```

<img src="http://wearemavens.com/images/mm/menu3.png"/>

Go to "MavensMate --> Open --> Settings - User" and modify "mm_workspace" with the location where you'd like your MavensMate projects to reside, for example (notice the absolute path):

	"mm_workspace": "/Users/your_username/Projects"

If you're using RVM, you probably want to update the "mm_ruby" setting:

	"mm_ruby": "~/.rvm/bin/rvm-auto-ruby"

##Update

```
$ ruby < <(curl -s https://raw.github.com/joeferraro/MavensMate-SublimeText/master/install.rb)
```

##Screenshots

###Project Wizard
<img src="http://wearemavens.com/images/mm/project_wizard.png"/>
###Apex Test Runner
<img src="http://wearemavens.com/images/mm/test2.png"/>