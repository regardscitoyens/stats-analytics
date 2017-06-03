#!/bin/bash

cd $(echo $0 | sed 's#/[^/]*$##')

source /usr/local/bin/virtualenvwrapper.sh > /dev/null 2>&1
workon analytics > /dev/null 2>&1

git pull > /tmp/load_stats_analytics.tmp 2>&1

./collect.py >> /tmp/load_stats_analytics.tmp 2>&1

if git status | grep "data/" > /dev/null; then
  cat /tmp/load_stats_analytics.tmp
  git add data
  git commit -m "autoupdate"
  git push
fi
