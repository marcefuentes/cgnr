#!/bin/bash

remote="cesga"
local_folder="$HOME/code/gnr/results" # source
remote_folder="/home/ulc/ba/mfu/code/gnr/" # destination

files="*.png"

rsync --recursive --verbose --progress --compress --times --rsh=ssh --include="*/" --include=$files --exclude="*" $local_folder $remote:$remote_folder

files="*.gif"

rsync --recursive --verbose --progress --compress --times --rsh=ssh --include="*/" --include=$files --exclude="*" $local_folder $remote:$remote_folder
