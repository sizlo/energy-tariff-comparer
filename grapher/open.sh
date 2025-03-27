#!/bin/bash
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

# Allow loading the csv files from disk
args="--allow-file-access-from-files"

# Run chrome in a new instance, otherwise it will open the
# page in an existing instance which does not allow local file access
if [ ! -d /tmp/grapher ]; then
  mkdir -p /tmp/grapher;
fi
args="$args --user-data-dir=/tmp/grapher"

# Open the grapher page on launch
args="$args --usr-data-dir=/tmp $SCRIPT_DIR/grapher.html"

# Don't open any welcome/sign in pages
args="$args --disable-fre --no-default-browser-check --no-first-run"

/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome $args > /dev/null 2>&1 &
