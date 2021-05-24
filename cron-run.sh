#!/bin/bash

PID_FILE=".pid"

# Activate python virtual env
source /home/bekeenin/virtualenv/wolvbot.bekeenin.com/wolvbot/3.8/bin/activate && cd /home/bekeenin/wolvbot.bekeenin.com/wolvbot

# Check latest commit on remote branch
remote_commit_id=`git rev-parse origin/main`

# Check latest deployment commit hash
latest_commit_id=`git rev-parse HEAD`

# Pull latest commit if there is any new commit
if [ "$remote_commit_id" != "$latest_commit_id" ]; then
    git checkout $remote_commit_id
    
    # Install required dependecies
    pip install -r requirements.txt
fi

# Check if there is a running instance
if test -f "$PID_FILE"; then
    kill -9 `cat $PID_FILE`
fi

nohup python bot.py &
echo $! > $PID_FILE