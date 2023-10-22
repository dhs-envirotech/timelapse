import os

os.system("sudo apt install ffmpeg imagemagick")

projectDirectory="/home/pi/timelapse"

# Custom Media Directory
# possibleNewProjectDirectory = input("The project directory is where the media folder is located.\nRelative to /home/pi, where is the project directory (timelapse)? ")
# if len(possibleNewProjectDirectory) > 0:
#     if possibleNewProjectDirectory.startswith("/") == True:
#         print("⚠️ Please provide a relative path. It cannot start with /")
#         exit(1)
    
#     projectDirectory = projectDirectory + possibleNewProjectDirectory

# print("Using %s..." % projectDirectory)

if not os.path.exists(projectDirectory):
    if os.path.exists("/home/pi/timelapse" + ".tar.gz"):
        os.system("tar -xzf timelapse.tar.gz")
    else:
        print('Please transfer timelapse.tar.gz onto this machine')
        exit(1)

webServer = f"@reboot pi bash {projectDirectory}/scripts/server.sh"
picture = f"*/15 * * * * pi bash {projectDirectory}/scripts/picture.sh {projectDirectory}/media"
video = f"3 * * * * pi bash {projectDirectory}/scripts/video.sh {projectDirectory}/media"

with open("/etc/cron.d/timelapse", "w") as file:
    file.write(webServer + "\n" + picture + "\n" + video)

os.system(f"sudo chmod +x {projectDirectory}/scripts/picture.sh {projectDirectory}/scripts/video.sh")