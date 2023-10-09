import os

os.system("sudo apt install ffmpeg imagmagick")

projectDirectory="/home/pi/timelapse/"

# Custom Media Directory
# possibleNewProjectDirectory = input("The project directory is where the media folder is located.\nRelative to /home/pi, where is the project directory (timelapse)? ")
# if len(possibleNewProjectDirectory) > 0:
#     if possibleNewProjectDirectory.startswith("/") == True:
#         print("⚠️ Please provide a relative path. It cannot start with /")
#         exit(1)
    
#     projectDirectory = projectDirectory + possibleNewProjectDirectory

# print("Using %s..." % projectDirectory)

if not os.path.exists(projectDirectory):
    os.system("tar -xzf timelapse.tar.gz")

pictureCron = "*/15 * * * * pi %sscripts/picture.sh %smedia" % (projectDirectory, projectDirectory)
videoCron = "# 3 * * * * pi %sscripts/video.sh %smedia" % (projectDirectory, projectDirectory)

with open("/etc/cron.d/timelapse", "w") as file:
    file.write(pictureCron + "\n" + videoCron)