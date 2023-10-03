#/bin/bash

cd frontend
npm run build
echo "
"
cd ..

echo "Built Frontend"

cd server
# Normal, automatic platform detection or force architecture
# go build
env GOOS=linux GOARCH=arm go build
cd ..

echo "Built Server"

rm -rf output
mkdir output output/scripts

echo "Reset output directory"

mv frontend/dist output/web
mv server/main output/server
cp server/scripts/* output/scripts

echo "Copied components to 'output' directory"

mkdir output/media output/media/pictures output/media/videos 
echo "Scaffoled media folder"

# Package
tar -czf output.tgz output