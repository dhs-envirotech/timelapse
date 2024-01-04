# Transfer `timelapse` code from personal computer

Instructions on how to prepare the code on your computer and then transfering to the Pi

> Use these instructions only if you don't have an interent connection to the Pi.

1. Clone the repository && `cd`
```bash
git clone https://github.com/dhs-envirotech/timelapse
cd timelapse
```
2. Zip the code
```bash
tar -czf timelapse.tar.gz src
```
3. Transfer the code with your Pi's specific hostname/IP
```bash
scp timelapse.tar.gz timelapse.py pi@raspberrypi.local:/home/pi
```
4. `ssh` into Pi
5. Go to step 4 of the original instructions