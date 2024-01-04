import os

if 'SUDO_UID' not in os.environ.keys():
    print('Run this script with sudo!')
    exit(1)

os.system('sudo apt-get -y update && sudo apt-get -y upgrade && sudo apt-get -y install imagemagick python3-opencv python3-flask ffmpeg')

projectDirectory="/home/pi/timelapse"

if not os.path.exists(projectDirectory):
    if os.path.exists("timelapse.tar.gz"):
        os.system("tar -xzf timelapse.tar.gz timelapse")
    else:
        print('Please transfer timelapse.tar.gz onto this machine')
        exit(1)

jobs = [
    f"@reboot pi bash {projectDirectory}/scripts/server.sh",
    # Every 3 hours, minute 0
    f"0 */3 * * * pi bash {projectDirectory}/scripts/picture.sh",
    # At minute 2, midnight
    f"2 0 * * * pi bash {projectDirectory}/scripts/video.sh",
    # 
    f"5 0 * * * pi bash {projectDirectory}/scripts/archive.sh"
]

with open("/etc/cron.d/timelapse", "w") as file:
    file.write('\n'.join(jobs) + '\n')

os.system(f"sudo chmod +x {projectDirectory}/scripts/picture.sh {projectDirectory}/scripts/video.sh")