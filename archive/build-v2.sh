#/bin/bash

# Make copy for build
cp -r src timelapse

# Cleanup
cd timelapse
rm -rf __pycache__
rm **/*/.DS_Store
rm media/pictures/*
rm media/*.mp4
rm media/archives/*
cd ..

# Package
tar -czf timelapse.tar.gz timelapse
rm -rf timelapse