#/bin/bash

output="timelapse"

# cd frontend
# npm run build
# cd ..

# if [ $? ]; then
#     clear
# fi

cd server
# Normal, automatic platform detection or force architecture
# go build
env GOOS=linux GOARCH=arm go build
cd ..

rm -rf $output
mkdir $output $output/scripts

# mv frontend/dist $output/web
mv server/main $output/server
cp server/scripts/* $output/scripts

mkdir $output/media $output/media/pictures $output/media/videos 
cp server/media/videos/ffmpeg.txt $output/media/videos/ffmpeg.txt

# Package
tar -czf $output.tar.gz $output
rm -rf $output