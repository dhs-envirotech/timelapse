import os

media = '/home/pi/timelapse/media'
pictures = f'{media}/pictures'
videos = f'{media}/videos'
video = f'{videos}/timelapse.mp4'

# Get pictures to be archived (sorted alphabetically)
pictures_list = sorted(os.listdir(pictures))
if not pictures_list:
    print('No pictures to archive!')

# "Calculate" zip name
end_timestamp = pictures_list[-1].replace('timelapse-', '').replace('.jpg', '')
zip_name = f'{media}/archives/media-{end_timestamp}.zip'

# Archive Video (copy video to timestamped name)
archived_video_name = f'timelapse-{end_timestamp}.mp4'
os.system(f'cp {video} {videos}/{archived_video_name}')

# Archive Pictures (copy timestamped video to pictures to be zipped)
os.system(f'cp {videos}/{archived_video_name} {pictures}/{archived_video_name}')
os.system(f'zip -r {zip_name} {pictures}')

# Reset pictures
os.system(f'rm -rf {pictures}')
os.system(f'mkdir {pictures}')