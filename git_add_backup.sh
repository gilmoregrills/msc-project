#!/bin/bash
#Script to rsync to Dropbox folder, and commit/push to github
#usage: ./git_add_backup.sh "commit message here" gitUsername gitPassword
#Obviously alias it to something more memorable 

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
git push 'https://'$2':'$3'@github.com/gilmoregrills/msc-project.git'
