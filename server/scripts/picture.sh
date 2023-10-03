#/bin/bash

# media folder. NOT video or picture folder!
if [ ! -d "$1" ];
then
    echo "'$1' does not exist. Please pass in a valid media folder as the first argument."
    exit 1
fi

$pictures="$1/pictures"

descending=$(date +"%Y.%m.%d.%H.%M")
formatted=$(date +"%B %d, %Y\n%H:%M:%S")

filename="$pictures/timelapse-$descending-raw.jpg"

# Raspberry Pi
raspistill -o $filename

# MacOS (brew install imagesnap)
# imagesnap $filename

# Imagemagick Tool
convert $filename -pointsize 36 -fill red -annotate +100+100 "$formatted" "$pictures/timelapse-$descending.jpg"

rm $filename