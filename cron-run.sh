#!/bin/bash

source /home/bekeenin/virtualenv/wolvbot.bekeenin.com/wolvbot/3.8/bin/activate && cd /home/bekeenin/wolvbot.bekeenin.com/wolvbot
git pull origin main
python bot.py