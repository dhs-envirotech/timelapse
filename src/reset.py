import os
import datetime

confirmation = input("Are you sure you want to erase all pictures & videos? (type 'delete')\n> ")

if confirmation != 'delete':
    print("Aborted")
    exit(0)

current_dirname = os.path.dirname(__file__)
log_file = current_dirname + '/reset_logs.txt'
if not os.path.exists(log_file):
    os.system('touch ' + log_file)

# Delete Files
pictures = f"{current_dirname}/media/pictures"
if os.listdir(pictures):
    os.system(f'sudo rm {pictures}/*')

videos = f"{current_dirname}/media/videos"
if os.listdir(videos):
    os.system(f'sudo rm {videos}/*')

with open(log_file, 'a') as file:
    file.write(str(datetime.datetime.now()) + '\n')