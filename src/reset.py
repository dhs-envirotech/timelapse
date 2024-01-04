import os, datetime, logging

confirmation = input("Are you sure you want to erase all pictures & videos? (type 'delete')\n> ")

if confirmation != 'delete':
    print("Aborted")
    exit(0)

logging.baseConfig(file='server.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logging.info(f'Attempting reset media at {datetime.datetime.now()}')

current_dirname = os.path.dirname(__file__)

# Delete Files
pictures = f"{current_dirname}/media/pictures"
if os.listdir(pictures):
    os.system(f'sudo rm {pictures}/*')

videos = f"{current_dirname}/media/videos"
if os.listdir(videos):
    os.system(f'sudo rm {videos}/*')

logging.info(f'Finished reset media')