#!/bin/bash
#Script to copy parent directory into Dropbox directory for back up
#can/should be aliased onto the git add or git commit commands.

#rsync to dropbox folder
CURRENT_DIRECTORY=$(pwd)
BACKUP_DIRECTORY=~/Dropbox/project_backup
cd ..
echo $CURRENT_DIRECTORY
echo $BACKUP_DIRECTORY

rsync --exclude-from=$CURRENT_DIRECTORY'/git_add_backup.sh' -ra $CURRENT_DIRECTORY $BACKUP_DIRECTORY

#add/commit/push to github!
cd $CURRENT_DIRECTORY
git status
git add -A
git status
echo $1
git commit -m "$1"
git push -u origin master
