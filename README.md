# timelapse

This codebase is all the code & infrastructure needed to turn a Raspberry Pi into a timelapse camera.

> It also runs its own access point (basically a wifi network) to allow access to the web server.

### Technologies Used

<!-- Variables -->
[tutorial]: https://www.raspberrypi.com/documentation/computers/configuration.html#before-you-begin
[Golang]: https://go.dev/
[fireship_Go_video]: https://www.youtube.com/watch?v=446E-r0rXHI
[Echo]: https://echo.labstack.com/
[Vite]: https://vitejs.dev/
[PicoCSS]: https://picocss.com/
[ImageMagick]: https://imagemagick.org/index.php
[ffmpeg]: https://ffmpeg.org/


- [Golang]: This is a programming language developed by Google as a compiled modern version of low-level languages like C. See [Fireship's video][fireship_Go_video] for more info. This is used to host the web server and can be cross-compiled to a Pi with the right cli args. Although the language is Go instead of Python, the web framework is [Echo] instead of Flask, one of the many options for hosting a HTTP server.
- `Frontend`: The frontend is decoupled from the server and is combined at build/package time. It uses a variety of technologies that are fairly familiar to web developers. First, for better DX, the build/dev tool is [Vite] (made by the same developer as VueJS!). No javascript framework is necessary so pure javascript for now. For styling, I utilized [PicoCSS].
- `Bash`: Although the previous version of this project uses Perl as the low-level Linux "commander", I am sticking with Bash. A cron job triggers `picture.sh` to take a picture with `raspistill`. The twist I added however is to leverage [ImageMagick] to add the timestamp of the image onto the image itself which makes testing and viewing much more descriptive. For making the videos, another cron job triggers `video.sh` which first, makes a timelapse from the pictures found in the pictures directory. It then deletes these pictures as they are no longer needed. It then checks for a previous timelapse to combine with the new one. It then renames and whatnot and spits out `timelapse.mp4` which can be viewed from the web server. The video mainpulating software is [ffmpeg]

If anything is missing here that is in the codebase, please open an issue.

### Other Notes

- `build.sh` does what it sounds like. It builds the Go server and the website and merges them into the `output` folder. Inside, the args needed for cross compilation are by default specified so the binary cannot be run on your personal computer.