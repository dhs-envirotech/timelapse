#/bin/bash

# Remove Preview Image
sudo rm /home/pi/timelapse/media/pictures/preview.jpg

pictures="/home/pi/timelapse/media/pictures"
videos="/home/pi/timelapse/media/videos"

# Make way for new timelapse while preserving old just in case
cd $videos
mv timelapse.mp4 old-timelapse.mp4

# Make the video :)
cd $pictures
ffmpeg -hide_banner -loglevel error -pattern_type glob -r 3 -i "*.jpg" -s 820x616 -vcodec libx264 "$videos/timelapse.mp4"
