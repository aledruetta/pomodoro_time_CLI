#!/usr/bin/env bash

source `which virtualenvwrapper.sh`

POMODORO=$HOME/Devel/pomodoro

cd $POMODORO
workon pomodoro
$POMODORO/pomodoro.py &
deactivate pomodoro
