# Native Python Libraries
import os
import socket
import re
import subprocess
from datetime import datetime
import time
import json

# Flask
from flask import Flask, render_template, send_file, send_from_directory, request

# Flask App
app = Flask(__name__, static_folder="static")

# Metadata
isRaspberryPi = False
try:
    isRaspberryPi = 'not found' not in str(subprocess.check_output(['which', 'raspistill']))
except subprocess.CalledProcessError:
    pass

hostname = socket.gethostname().replace('.local', '').replace('.lan', '')
title = hostname
try:
    title = 'Raspberry Pi ' + str(int(hostname[-1]))
except ValueError:
    pass

# Logging
def log_set_time(log):
    with open(set_time_log_file, 'r') as file:
        json_data = json.load(file)
    json_data.append(log)
    with open(set_time_log_file, 'w') as file:
        json.dump(json_data, file)

# Create log file if it doesn't exist
set_time_log_file = app.root_path + '/set_time_logs.json'
if not os.path.exists(set_time_log_file):
    with open(set_time_log_file, 'w') as file:
        file.write('[]')

videos = app.root_path + '/media/videos'

# Homepage
@app.route('/')
def index():
    return render_template('index.html', title=title, videos=sorted(os.listdir(videos)))


# Time Management
@app.route('/api/time', methods=['GET'])
def server_time():
    return str(int(time.time() * 1000))

set_time_last_call = None
date_regex = r"^\d{2}\/\d{2}\/\d{4} \d{2}:\d{2}:\d{2}$"
@app.route('/api/time', methods=['POST'])
def set_time():
    # Rate limiting
    global set_time_last_call
    if set_time_last_call is None:
        set_time_last_call = datetime.now()
    else:
        diff = datetime.now() - set_time_last_call
        if diff.total_seconds() < 5:
            return 'too many requests in 5 seconds', 429
        else:
            set_time_last_call = datetime.now()

    # Verify
    string = str(request.data, 'utf8')
    match = re.search(date_regex, string)
    if not match:
        return 'Invalid format', 400
    # Log (security)
    log_set_time({
        'ip': request.remote_addr,
        'old_time': datetime.now().strftime('%m/%d/%Y %H:%M:%S'),
        'new_time': string
    })
    # Perform
    if isRaspberryPi:
        os.system(f'sudo date -s "{string}"')

    return server_time(), 200

# Preview Image
already_taking = False
take_preview_image_last_call = None
@app.route('/api/take-preview-image', methods=['POST'])
def take_preview_image():
    # Rate limiting
    global take_preview_image_last_call, already_taking
    if take_preview_image_last_call is None:
        take_preview_image_last_call = datetime.now()
    else:
        diff = datetime.now() - take_preview_image_last_call
        if diff.total_seconds() < 5:
            return 'too many requests in 5 seconds', 429
        else:
            take_preview_image_last_call = datetime.now()

    # Don't allow around the 2 minute mark (same as cron job, give or take 2)
    if abs(datetime.now().minute - 2) < 2:
        return 'Time reserved! A preview image cannot be taken at this time.', 400
    
    if already_taking:
        return 'Already taking a preview image', 400

    # Take picture
    already_taking = True
    if isRaspberryPi:
        os.system('sudo raspistill -o /home/pi/timelapse/media/pictures/preview.jpg')
    else:
        os.system(f'imagesnap {app.root_path}/media/pictures/preview.jpg')
    already_taking = False

    return 'Image taken', 200

# Pictures & Archives
folders = ['Pictures', 'Archives']
folders_lowercase = ['pictures', 'archives']

@app.route('/<path:folder>')
def folder_page(folder):
    if folder not in folders_lowercase:
        return 'Folder not found', 404
    return render_template('directory.html', folder=folder, folder_uppercase=folders[folders_lowercase.index(folder)], files=os.listdir(app.root_path + '/media/' + folder))

@app.route('/<path:folder>/<path:file>')
def folder_file(folder, file):
    if folder not in folders_lowercase and folder != 'videos':
        return 'Folder not found', 404
    response = send_from_directory(app.root_path + '/media/' + folder, file)
    response.headers['Cache-Control'] = 'no-cache'
    return response

    
# Videos
# videos = app.root_path + '/media/videos/'
# @app.route('/video/<path:name>')
# def video(name):
#     response = send_from_directory(videos, name)
#     response.headers['Cache-Control'] = 'no-cache'
#     return response

# video_file = app.root_path + '/media/timelapse.mp4'
# @app.route('/video')
# def video():
#     if not os.path.exists(video_file):
#         return bytes('Error: ' + video_file + ' does not exist... :(<br><br><a href="/">Go back</a>', 'utf-8')
#     return send_file(video_file, mimetype="video/mp4")

# Run!
if __name__ == '__main__':
    app.run(debug=(not isRaspberryPi), host="0.0.0.0")