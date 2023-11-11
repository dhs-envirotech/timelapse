# timelapse

This codebase is all the code & infrastructure needed to turn a Raspberry Pi into a timelapse camera.

### Usage
0. [Setup the Pi](https://github.com/orgs/dhs-envirotech/discussions/6)
1. Connect the camera to the Pi
2. Clone the repo on your computer and run `build.sh` with the following command:
```bash
bash build.sh
```
3. Transfer the bundle and the setup script to the Pi
```bash
scp timelapse.tar.gz setup-timelapse.py pi@raspberrypi.local:/home/pi
```
4. Run the setup script. It will unpack `timelapse.tar.gz` if necessary install all the packages needed, and write (or overwrite) a new crontab at `/etc/cron.d/timelapse`. Takes effect immediately.
```bash
sudo python3 setup-timelapse.py
```
5. Restart the computer
```bash
sudo reboot now
```

### Other Notes

- `build.sh` does what it sounds like. It builds the Go server and the website and merges them into the `output` folder. Inside, the args needed for cross compilation are by default specified so the binary cannot be run on your personal computer.

### Technologies Used

<!-- Variables -->
[tutorial]: https://www.raspberrypi.com/documentation/computers/configuration.html#before-you-begin
[PicoCSS]: https://picocss.com/
[ImageMagick]: https://imagemagick.org/index.php
[opencv]: https://opencv.org/

- `Frontend`: This project uses Flask to serve and a simple single page website (styled with [PicoCSS]).
There is a hidden route `/date` which provides a date command to set the date on the raspberry pi. Meant for an admin with an SSH session
- `Bash`: Although the previous version of this project uses Perl as the low-level Linux "commander", I am sticking with Bash. A cron job triggers `picture.sh` to take a picture with `raspistill`. The twist I added however is to leverage [ImageMagick] to add the timestamp of the image onto the image itself which makes testing and viewing much more descriptive. For making the videos, another cron job triggers `video.sh` which first, makes a timelapse from the pictures found in the pictures directory. It then deletes these pictures as they are no longer needed. It then checks for a previous timelapse to combine with the new one. It then renames and whatnot and spits out `timelapse.mp4` which can be viewed from the web server. The video mainpulating software is [opencv]

If anything is missing here that is in the codebase, please open an issue.