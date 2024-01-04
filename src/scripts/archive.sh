#!/bin/bash

# sudo python3 /home/pi/timelapse/scripts/archive.py

MEDIA="/home/pi/timelapse/media"
PICTURES="$MEDIA/pictures"
VIDEOS="$MEDIA/videos"
VIDEO="$VIDEOS/timelapse.mp4"

TIMESTAMP=$(date +"%Y.%m.%d.%H.%M")
ZIP_NAME="$MEDIA/archives/media-$TIMESTAMP.zip"

# Archive Video (copy video to timestamped name)
ARCHIVED_VIDEO_NAME="timelapse-$TIMESTAMP.mp4"
sudo cp $VIDEO "$VIDEOS/$ARCHIVED_VIDEO_NAME"

# Archive Pictures (copy timestamped video to pictures to be zipped)
sudo cp $VIDEOS/$ARCHIVED_VIDEO_NAME $PICTURES/$ARCHIVED_VIDEO_NAME
cd $MEDIA
sudo zip -r $ZIP_NAME pictures

# Remove pictures
sudo rm -rf $PICTURES
sudo mkdir $PICTURES