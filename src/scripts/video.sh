#!/bin/bash

# Remove Preview Image
sudo rm /home/pi/timelapse/media/pictures/preview.jpg

# Run Python Script
# sudo python3 /home/pi/timelapse/scripts/video.py

media="/home/pi/timelapse/media"
pictures="$media/pictures"
videos="$media/videos"

# Rename current video
cd $videos
sudo rm old-timelapse.mp4
sudo mv timelapse.mp4 old-timelapse.mp4

# Make new video
cd $pictures
sudo ffmpeg -hide_banner -loglevel error -pattern_type glob -r 1 -i "*.jpg" -s 820x616 -vcodec libx264 "$videos/timelapse.mp4"

# # Move old images to archive buffer
mv '*.jpg' "$archivebuffer/"

# # There should be 2 video files in the media folder: old-timelapse.mp4 & new-timelapse.mp4

# cd $media
# echo "file old-timelapse.mp4
# file new-timelapse.mp4" > video.txt
# ffmpeg -f concat -safe 0 -i video.txt -c copy timelapse.mp4