#!/bin/bash
curl -s https://mavensmate-app-auto-updater.herokuapp.com/download/channel/beta/osx > mm.zip
unzip -a mm.zip
sudo cp -R MavensMate.app /Applications
open /Applications/MavensMate.app