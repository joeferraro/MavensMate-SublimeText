MavensMate users,

I want to apologize for any inconvenience the past week and a half may have caused you. Last Tuesday, v5.0.0 of the Sublime Text plugin was pushed to the Package Control release channel, which automatically upgraded many developers unexpectedly. Not only were they upgraded, they were greeted with an unfamiliar error message stating that they needed to download a new companion app called MavensMate-app. This application has been in development and testing for nearly 8 months and was heavily tested on OS X, Linux, and Windows. Unfortunately, several major issues were uncovered, which have left me working virtually around the clock to diagnose and patch edge cases related to compile times, proxies, permissions, antivirus software ... the list goes on. 

This message is to let you know that I've decided to roll the Sublime Text plugin release channel back to its former state, v4.0.5 until the multitude of v5 issues can be dealt with.

Starting tomorrow, Package Control will start to automatically update MavensMate to v6.0.0, which will actually be v4.0.5. If you would NOT like to be updated to v6, you MUST add "MavensMate" to your "auto_upgrade_ignore" Package Control Settings (e.g. "auto_upgrade_ignore" : [ "MavensMate" ]). Once v6 has been installed, you will need to re-configure your user settings as you did in v4.0.5. For those that wish to continue using v5, we will host it as v7 in the Package Control beta channel. If you would like to install these prereleases, you must add "MavensMate" to your "install_prereleases" Package Control setting (e.g. "install_prereleases" : [ "MavensMate" ]).

For those that have spent their time helping me diagnose and patch issues, I truly appreciate it. For those that have taken this opportunity to disrespect me or any other MavensMate contributor, I would ask that you direct your negative energy elsewhere.

Sincerely,

Joe

### Instructions for updating to v6

By tomorrow, I will push v6 (which will actually be v4.0.5) to the Package Control release channel. You will automatically be updated. Once installed, you should update your plugin user settings (like `mm_workspace`) and you should be back to the state you were in before updating to v5.

### Instructions for testing v7 (formerly v5)

v7 will be available only in the Package Control **prerelease** channel. To install v7, you will need to add `"MavensMate"` to your `"install_prereleases"` Package Control Settings (see below):

![screen shot 2015-09-02 at 9 10 17 am](https://cloud.githubusercontent.com/assets/54157/9632003/79242b02-5152-11e5-8672-d91bb549cee6.png)
![package_control_sublime-settings_ _df15-react-communities-ios](https://cloud.githubusercontent.com/assets/54157/9632015/8cf6d800-5152-11e5-925e-627995a4aef5.png)
##Setup