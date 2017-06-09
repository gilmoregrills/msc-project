#!/bin/bash
#Script to copy parent directory into Dropbox directory for back up
#can/should be aliased onto the git add or git commit commands.

CURRENT_DIRECTORY=$(pwd)
BACKUP_DIRECTORY=~/Dropbox/project_backup
cd ..
echo $CURRENT_DIRECTORY
echo $BACKUP_DIRECTORY

rsync --exclude-from=$CURRENT_DIRECTORY'/git_add_backup.sh' -ra $CURRENT_DIRECTORY $BACKUP_DIRECTORY
