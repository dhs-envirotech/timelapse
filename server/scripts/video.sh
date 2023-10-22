#/bin/bash

# media folder. NOT video or picture folder!
if test -f "$1";
then
    echo "'$1' does not exist. Please pass in a valid media folder as the first argument."
    exit 1
fi

videos="$1/videos"
pictures="$1/pictures"

if [ ! -n "$(ls -A $pictures)" ]; then
    exit 0
fi

cd "$1/videos"

old_timelapse="$videos/old-timelapse.mp4"
new_timelapse="$videos/new-timelapse.mp4"
timelapse="$videos/timelapse.mp4"

sudo ffmpeg -hide_banner -loglevel error -y -framerate 1/3 -pattern_type glob -i "$pictures/*.jpg" "$new_timelapse"

if test -f "$timelapse";
then
    echo "Triggered"
    sudo mv $timelapse $old_timelapse
    
    sudo ffmpeg -hide_banner -loglevel -f concat -i "$1/videos/ffmpeg.txt" "$timelapse"
    sudo rm $old_timelapse $new_timelapse
else 
    sudo mv $new_timelapse $timelapse
fi


sudo rm -rf $pictures
sudo mkdir $pictures