import cv2
import os

if 'SUDO_UID' not in os.environ.keys():
    print('Run this script with sudo!')
    exit(1)

# Config
timelapse_dir = '/home/pi/timelapse'
timelapse_file = timelapse_dir + '/media/videos/timelapse.webm'
old_timelapse_file = timelapse_dir + '/media/videos/old-timelapse.webm'
frame_rate = 3

# Setup
image_dir = timelapse_dir + "/media/pictures"
image_files = sorted([os.path.join(image_dir, filename) for filename in os.listdir(image_dir) if filename.endswith(('.png', '.jpg', '.jpeg'))])
if not image_files:
    print("No image files found in the directory.")
    exit()

# Rename
if os.path.isfile(timelapse_file):
    os.rename(timelapse_file, old_timelapse_file)

# More setup
first_image = cv2.imread(image_files[0])
height, width, layers = first_image.shape
fourcc = cv2.VideoWriter_fourcc(*'VP80') 
output_video = cv2.VideoWriter(timelapse_file, fourcc, frame_rate, (width, height))

# Write!
if os.path.isfile(old_timelapse_file):
    old_timelapse_video = cv2.VideoCapture(old_timelapse_file)
    while old_timelapse_video.isOpened():
        r, frame = old_timelapse_video.read()
        if not r:
            break
        output_video.write(frame)

for image_file in image_files:
    frame = cv2.imread(image_file)
    output_video.write(frame)
    os.remove(os.path.join(image_dir, image_file))

# Finished!
output_video.release()