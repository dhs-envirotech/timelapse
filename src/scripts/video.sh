#/bin/bash

# Remove Preview Image
sudo rm /home/pi/timelapse/media/pictures/preview.jpg

# Run Python Script
# sudo python3 /home/pi/timelapse/scripts/video.py

pictures="/home/pi/timelapse/media/pictures"
videos="/home/pi/timelapse/media/videos"

cd videos
mv timelapse.mp4 old-timelapse.mp4

cd pictures
ffmpeg -hide_banner -loglevel error -pattern_type glob -r 3 -i "*.jpg" -s 820x616 -vcodec libx264 "$videos/timelapse.mp4"
# TODO: Archive images

cd videos
# TODO: combine videos