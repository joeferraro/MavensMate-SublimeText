# MavensMate for Sublime Text

MavensMate for Sublime Text is a plugin that aims to replicate the functionality of the Eclipse-based Force.com IDE. Its goal is to allow developers to work inside Sublime Text for all their Force.com-related tasks.

* Create & Edit Salesforce.com projects with specific package metadata
* Create & compile Apex Classes, Apex Trigger, Visualforce Pages, Visualforce Components
* Create & Edit Lightning Components (v7 only)
* Retrieve & compile other types of Salesforce.com metadata
* Run Apex test methods and visualize test successes/failures & coverage
* Deploy metadata to other Salesforce.com orgs
* Apex Execute Anonymous
* Stream Apex Logs to your local filesystem
* Apex & Visualforce Code Assist

## Issues

All issues are managed by the [central MavensMate project](https://github.com/joeferraro/MavensMate)

## Install

### Prerequisites

- Sublime Text 3 [http://www.sublimetext.com/3](http://www.sublimetext.com/3)
- Sublime Text Package Control [https://packagecontrol.io/installation](https://packagecontrol.io/installation)
- MavensMate Desktop **(must be running in order for MavensMate for Sublime Text v7.0+ to function)** [https://github.com/joeferraro/mavensmate-desktop/releases](https://github.com/joeferraro/mavensmate-desktop/releases)

### Plugin Installation

1. Open Sublime Text 3
2. Run `Package Control: Install Package` command
	- [Running commands from Sublime Text](http://docs.sublimetext.info/en/latest/extensibility/command_palette.html)
3. Search for `MavensMate`
4. Hit `Enter`

**IMPORTANT NOTE:** If you are interested in automatically installing prereleases, you must add `"MavensMate"` to your Package Control `"install_prereleases"` user setting, see below:

![screen shot 2015-09-02 at 9 10 17 am](https://cloud.githubusercontent.com/assets/54157/9632003/79242b02-5152-11e5-8672-d91bb549cee6.png)
![package_control_sublime-settings_ _df15-react-communities-ios](https://cloud.githubusercontent.com/assets/54157/9632015/8cf6d800-5152-11e5-925e-627995a4aef5.png)
![screen shot 2015-10-12 at 12 53 39 pm](https://cloud.githubusercontent.com/assets/54157/10433499/557e5134-70e0-11e5-81e5-8910ad6cdd68.png)


## Setup

### Important Settings (Configured in MavensMate Desktop)

#### Workspaces (mm_workspace)

You may set `mm_workspace` to a single path on your local filesystem or an array of paths.

##### Examples

###### Array of workspaces

```
"mm_workspace" : [
	"/Users/darylshaber/Desktop/my-cool-folder",
	"/Users/darylshaber/Workspaces/my-mavensmate-workspace"
],
```

###### Single workspace

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

## Update

Updates to the plugin are handled automatically by Package Control.

## Screenshots

### Project Wizard
<img src="https://mavens.com/public/mavensmate/img/new-project.png" style="box-shadow:-14px 14px 0 0 #16325c"/>
### Apex Test Runner
<img src="https://mavens.com/public/mavensmate/img/tests.png"/>
### Apex Execute Anonymous
<img src="https://mavens.com/public/mavensmate/img/execute-apex.png"/>
### Quick Panel
<img src="http://wearemavens.com/images/mm/panel.png"/>
### Apex/Visualforce Code Assist
<img src="https://mavens.com/public/mavensmate/img/apex2.png"/>
<img src="https://mavens.com/public/mavensmate/img/vf1.png"/>
<img src="https://mavens.com/public/mavensmate/img/vf2.png"/>

[mmcom]: http://mavensmate.com/?utm_source=github&utm_medium=st-plugin&utm_campaign=st
