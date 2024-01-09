#/bin/bash

# Remove Preview Image
sudo rm /home/pi/timelapse/media/pictures/preview.jpg

PICTURES="/home/pi/timelapse/media/pictures"
VIDEOS="/home/pi/timelapse/media/videos"

# Make "way" for the video
cd $VIDEOS
sudo mv timelapse.mp4 old-timelapse.mp4

# Make video
cd $PICTURES
sudo ffmpeg -hide_banner -loglevel error -pattern_type glob -r 3 -i "*.jpg" -s 820x616 -vcodec libx264 "$VIDEOS/new-timelapse.mp4"

# Combine with old video
cd $VIDEOS
sudo ffmpeg -hide_banner -loglevel error -f concat -safe 0 -i "$VIDEOS/ffmpeg.txt" -c copy timelapse.mp4

# KAEHMS

# #/bin/bash

# # This script uses ffmpeg to create a nightly or weekly video in mp4 format
# # from all jpgs in the pictures folder. If the "weekly" flag is passed to the
# # script, it will first create the video, then archive the existing jpgs into
# # a backup folder.

# # A nightly video (timelapse.mp4) is maintained in the videos directory.  If
# # run in weekly mode, a copy of the nightly video will be timestamped and 
# # maintained in the video directory as well.

# # paths and variables.  We should move this code into a config file used across
# # all related programs/scripts

# INSTALL_DIR="/home/pi"
# PICTURES=$INSTALL_DIR"/timelapse/media/pictures"
# VIDEOS=$INSTALL_DIR"/timelapse/media/videos"
# BACKUPS=$INSTALL_DIR"/timelapse/media/backups"
# DATESTAMP=$(date -I)


# cd $VIDEOS
# if [ -f ./timelapse.mp4 ]; then 
# mv timelapse.mp4 old-timelapse.mp4
# fi

# cd $PICTURES
# ffmpeg -hide_banner -loglevel error -pattern_type glob -r 3 -i "*.jpg" -s 820x616 -vcodec libx264 "$VIDEOS/timelapse.mp4"



# if [[ $1 == "weekly" ]]; then
#   cd $VIDEOS
#   cp timelapse.mp4 "timelapse-"$DATESTAMP".mp4"
#   cd $PICTURES
#   tar -cf $BACKUPS"/pictures-"$DATESTAMP".tar"  *.jpg
#   rm -f *.jpg
# fi