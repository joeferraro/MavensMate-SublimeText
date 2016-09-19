#!/bin/bash
curl -s https://mavensmate-app-auto-updater.herokuapp.com/download/channel/$2/osx > "$1/MavensMate.zip"
unzip -a "$1/MavensMate.zip" -d "$1"
rm -rf /Applications/MavensMate.app
cp -R "$1/MavensMate.app" /Applications
rm -rf "$1/MavensMate.zip"
rm -rf "$1/MavensMate.app"
open /Applications/MavensMate.app