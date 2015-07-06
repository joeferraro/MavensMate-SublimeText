#MavensMate for Sublime Text

MavensMate for Sublime Text is a plugin that aims to replicate the functionality of the Eclipse-based Force.com IDE. Its goal is to allow developers to work inside Sublime Text for all their Force.com-related tasks.

* Create & Edit Salesforce.com projects with specific package metadata
* Create & compile Apex Classes, Apex Trigger, Visualforce Pages, Visualforce Components, and Lightning Components
* Retrieve & compile other types of Salesforce.com metadata
* Run Apex test methods and visualize test successes/failures & coverage
* Deploy metadata to other Salesforce.com orgs
* Apex Execute Anonymous
* Create Apex Execution Overlay Actions "checkpoints" (tooling API)
* Stream Apex Logs to your local filesystem
* Apex & Visualforce Code Assist

####For detailed information and documentation, please visit [mavensmate.com][mmcom]

##Install

### Prerequisites 

**You must install the following before continuing:**

1. Sublime Text 3 [http://www.sublimetext.com/3](http://www.sublimetext.com/3)
2. Sublime Text Package Control [https://packagecontrol.io/installation](https://packagecontrol.io/installation)
3. Node.js [https://nodejs.org/download/](https://nodejs.org/download/)

###Installing the MavensMate node package

Type the following in a terminal/command prompt:

```
npm install mavensmate
```

**Note:** Depending on your operating system & security settings, you may need to run this command as an administrator. On Mac/Linux, you may run: `sudo npm install mavensmate`. On Windows, you may need to run the Command Prompt as an administrator.

- [How to open a terminal on Mac](http://blog.teamtreehouse.com/introduction-to-the-mac-os-x-command-line)
- [How to open a command prompt in Windows](http://windows.microsoft.com/en-us/windows-vista/open-a-command-prompt-window)
- [How to open a terminal on Ubuntu](https://help.ubuntu.com/community/UsingTheTerminal)


###Installing the MavensMate for Sublime Text package

1. Open Sublime Text 3
2. Run `Package Control: Install Package` command
	- [Running commands from Sublime Text](http://docs.sublimetext.info/en/latest/extensibility/command_palette.html)
3. Search for `MavensMate`
4. Hit `Enter`

##Setup

In order to get started using MavensMate for Sublime Text, you should be aware of a few important settings. MavensMate settings follow the Sublime Text convention of providing default settings in [JSON format](https://en.wikipedia.org/wiki/JSON) that can be overwritten via a user settings file. To view MavensMate default and user settings, use the MavensMate menu in the top menu bar: `MavensMate > Settings`.

###Important Settings

####mm_workspace

You must configure the `mm_workspace` setting before creating a new MavensMate project. You may set `mm_workspace` to a single path on your local filesystem or an array of paths.

#####Examples

######Array of workspaces

```
"mm_workspace" : [
	"/Users/darylshaber/Desktop/my-cool-folder",
	"/Users/darylshaber/Workspaces/my-mavensmate-workspace"
],
```

######Single workspace

```
"mm_workspace" : "/Users/darylshaber/Desktop/my-cool-folder",
```

**Windows users:** You must use escaped backslashes to set your workspaces:

```
"mm_workspace" : [
	"\\Users\\darylshaber\\Desktop\\my-cool-folder",
	"\\Users\\darylshaber\\Workspaces\\my-mavensmate-workspace"
],
```

####mm_api_version

Use `mm_api_version` to set your desired Salesforce.com API version. Please note, it should be set to a single decimal place:

#####Correct

```
"mm_api_version" : "33.0",
```

#####Incorrect

```
"mm_api_version" : 33,
```

##Update

Updates to the plugin are handled automatically by Package Control. Updates can be applied manually by replacing the `MavensMate` directory in your Sublime Text `Packages` directory.

##Documentation
<a href="MavensMate for Sublime Text Documentation">http://mavensmate.com/Plugins/Sublime_Text/Overview</a>

##Screenshots

###Project Wizard
<img src="http://cdn.mavensconsulting.com/mavensmate/img/new-project.png" style="box-shadow:-14px 14px 0 0 #16325c"/>
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

[mmcom]: http://mavensmate.com/?utm_source=github&utm_medium=st-plugin&utm_campaign=st
