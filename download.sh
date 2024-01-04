#!/bin/bash

cd /home/pi
git clone https://github.com/dhs-envirotech/timelapse
mv timelapse temp

mv temp/timelapse timelapse
mv temp/timelapse.py timelapse.py

echo "Download finished"