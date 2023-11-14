import os

if 'SUDO_UID' not in os.environ.keys():
    print('Run this script with sudo!')
    exit(1)

os.system('sudo apt-get -y update && sudo apt-get -y upgrade && sudo apt-get -y install imagemagick python3-opencv python3-flask')

projectDirectory="/home/pi/timelapse"

if not os.path.exists(projectDirectory):
    if os.path.exists("timelapse.tar.gz"):
        os.system("tar -xzf timelapse.tar.gz timelapse")
    else:
        print('Please transfer timelapse.tar.gz onto this machine')
        exit(1)

webServer = f"@reboot pi bash {projectDirectory}/scripts/server.sh"
picture = f"0 * * * * pi bash {projectDirectory}/scripts/picture.sh"
video = f"3 */3 * * * pi bash {projectDirectory}/scripts/video.sh"

with open("/etc/cron.d/timelapse", "w") as file:
    file.write(webServer + "\n" + picture + "\n" + video + "\n")

os.system(f"sudo chmod +x {projectDirectory}/scripts/picture.sh {projectDirectory}/scripts/video.sh")