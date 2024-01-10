# timelapse

This codebase is all the code & infrastructure needed to turn a Raspberry Pi into a timelapse camera.

## Usage
0. [Setup the Pi](https://github.com/orgs/dhs-envirotech/discussions/6)
1. Connect the camera to the Pi
2. Setup the camera (Interface -> Enable Legacy Camera -> Do not restart.)
```bash
sudo raspi-config
```
3. Run our download script to skip some file renaming and moving (otherwise, do it manually by following the script line by line)
```bash
curl -fsSL https://raw.githubusercontent.com/dhs-envirotech/timelapse/main/download.sh | sudo bash
```
4. Run the setup script. It will install all the packages needed, and write (or overwrite) a new crontab at `/etc/cron.d/timelapse`. Takes effect immediately.
```bash
sudo python3 timelapse.py setup
```
5. Restart the computer
```bash
sudo reboot now
```

## Other Notes

- `build.sh` takes the `src` directory and compresses it for `scp`
- To force a sync in the browser time, open the JS console in the web page and run `syncServerTime()`
- A preview image cannot be taken in the first minutes of the hour to keep the camera free for the cron scripts.

### Framerate
To change the frame rate of the video, there are 2 things to consider. 
1. The `frame_rate` variable in `video.py` controls the actual framerate
2. To supply the right amount of frames, the cron jobs in `setup-timelapse.py` need to be modified.

View the cron config in `timelapse.py`

If the frame rate represents the # of frames present at video compile time, there will a smooth, equal # of frames per second.

### Technologies Used

<!-- Variables -->
[PicoCSS]: https://picocss.com/
[ImageMagick]: https://imagemagick.org/index.php
[ffempg]: https://ffmpeg.org/

- `Frontend`: This project uses Flask to serve and a simple single page website (styled with [PicoCSS]).
- `Bash`: Although the previous version of this project uses Perl as the low-level Linux "commander", I am sticking with Bash. A cron job triggers `picture.sh` to take a picture with `raspistill`. A twist I added, however, is to leverage [ImageMagick] to add the timestamp of the image onto the image itself which makes testing and viewing much more descriptive. For making the videos, another cron job triggers `video.sh` which first, makes a timelapse from the pictures found in the pictures directory. It deletes these pictures as they are no longer needed and then checks for a previous timelapse to combine with the new one. Finally, the video is renamed to `timelapse.mp4` which can be viewed from the web server. The video mainpulating software is [ffmpeg]

> If anything is missing here that is in the codebase, please open an issue
