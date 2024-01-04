#!/bin/bash

# Skip this for manual walk-through
if ! command -v git &> /dev/null; then
    echo "Git is not installed. Run 'sudo apt install git'"
    exit 1
fi

cd /home/pi
git clone https://github.com/dhs-envirotech/timelapse
mv timelapse temp

mv temp/src timelapse
mv temp/timelapse.py timelapse.py
rm -rf temp

echo "Download finished"