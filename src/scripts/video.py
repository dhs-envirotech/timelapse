import cv2
import os
import socket

# Config
timelapse_dir = '/home/pi/timelapse' if 'raspberrypi' in socket.gethostname() else '/Users/humanfriend22/dev/dhs-envirotech/test'
timelapse_file = timelapse_dir + '/media/videos/timelapse.webm'
old_timelapse_file = timelapse_dir + '/media/videos/old-timelapse.webm'
frame_rate = 1/3

# Rename
if os.path.isfile(timelapse_file):
    os.rename(timelapse_file, old_timelapse_file)

# Setup
image_dir = timelapse_dir + "/media/pictures"
image_files = sorted([os.path.join(image_dir, filename) for filename in os.listdir(image_dir) if filename.endswith(('.png', '.jpg', '.jpeg'))])
if not image_files:
    print("No image files found in the directory.")
    exit()
first_image = cv2.imread(image_files[0])
height, width, layers = first_image.shape
fourcc = cv2.VideoWriter_fourcc(*'VP80') 
output_video = cv2.VideoWriter(timelapse_file, fourcc, frame_rate, (width, height))

# Write!
# if os.path.isfile(old_timelapse_mp4):
#     old_timelapse_video = cv2.VideoCapture(old_timelapse_mp4)
#     while old_timelapse_video.isOpened():
#         r, frame = old_timelapse_video.read()
#         if not r:
#             break
#         output_video.write(frame)

for image_file in image_files:
    frame = cv2.imread(image_file)
    output_video.write(frame)
    os.remove(os.path.join(image_dir, image_file))

# Finished!
output_video.release()