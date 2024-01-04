import os, sys, logging, datetime

if 'SUDO_UID' not in os.environ.keys():
    print('Run this script with sudo!')
    exit(1)

if len(sys.argv) == 1:
    print("Please provide action: 'setup' or 'reset'")
    exit(1)
elif sys.argv[1] == 'reset':
    confirmation = input("Are you sure you want to erase all media? (type 'delete')\n> ")

    if confirmation != 'delete':
        print("Aborted")
        exit(0)

    logging.basicConfig(filename='src/server.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
    logging.info(f'Attempting reset media')

    current_dirname = os.path.dirname(__file__)

    # Delete Files
    media = f"{current_dirname}/timelapse/media"
    os.system(f'sudo rm -rf {media}')
    os.system(f'mkdir {media}')

    logging.info('Finished reset media')
elif sys.argv[1] != 'setup':
    print("Please provide action: 'setup' or 'reset'")
    exit(1)

os.system('sudo apt-get -y update && sudo apt-get -y upgrade && sudo apt-get -y install imagemagick python3-opencv python3-flask ffmpeg')

projectDirectory="/home/pi/timelapse"

if not os.path.exists(projectDirectory):
    if os.path.exists("timelapse.tar.gz"):
        os.system("tar -xzf timelapse.tar.gz timelapse")
    else:
        print('Please transfer timelapse.tar.gz to this computer')
        exit(1)

jobs = [
    f"@reboot pi bash {projectDirectory}/scripts/server.sh",
    # Every 3 hours, minute 0
    f"0 */3 * * * pi bash {projectDirectory}/scripts/picture.sh",
    # At minute 2, midnight
    f"2 0 * * * pi bash {projectDirectory}/scripts/video.sh",
    # At minute 5, midnight
    f"5 0 * * * pi bash {projectDirectory}/scripts/archive.sh"
]

with open("/etc/cron.d/timelapse", "w") as file:
    file.write('\n'.join(jobs) + '\n')

os.system(f"sudo chmod +x {projectDirectory}/scripts/picture.sh {projectDirectory}/scripts/video.sh")