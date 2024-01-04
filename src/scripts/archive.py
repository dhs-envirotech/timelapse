import os

media = '/home/pi/timelapse/media'
video = f'{media}/timelapse.mp4'
pictures = f'{media}/pictures'
videos = f'{media}/videos'

# Get pictures to be archived (sorted alphabetically)
pictures_list = sorted(os.listdir(pictures))
if not pictures_list:
    print('No pictures to archive!')

# "Calculate" zip name
end_timestamp = pictures_list[-1].replace('timelapse-', '').replace('.jpg', '')
zip_name = f'{media}/archives/media-{end_timestamp}.zip'

# Archive Video
os.system(f'cp {video} {videos}/timelapse-{end_timestamp}.mp4')

# Archive Pictures (with video)
os.system(f'mv {video} {pictures}')
os.system(f'zip -r {zip_name} {pictures}')

# Reset pictures
os.system(f'rm -rf {pictures}')
os.system(f'mkdir {pictures}')