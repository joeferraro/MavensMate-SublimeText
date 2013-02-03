#!/bin/sh
mkdir -p ../User
mkdir -p /tmp/mm-workspace
sed "s/\"mm_workspace\" : \"\"/\"mm_workspace\" : \"\/tmp\/mm-workspace\"/g" mavensmate.sublime-settings > ../User/mavensmate.sublime-settings