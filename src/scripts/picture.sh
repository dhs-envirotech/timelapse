#/bin/bash

pictures="/home/pi/timelapse/media/sudo apt-get install python-pippictures"

descending=$(date +"%Y.%m.%d.%H.%M")
formatted=$(date +"%B %d, %Y\n%H:%M:%S")

filename="$pictures/timelapse-$descending-raw.jpg"

# Raspberry Pi
sudo libcamera-jpeg -v 0 -o $filename

# MacOS (brew install imagesnap)
# imagesnap $filename

# Imagemagick Tool
sudo convert $filename -pointsize 36 -fill red -annotate +100+100 "$formatted" "$pictures/timelapse-$descending.jpg"

sudo rm $filename