# Native Python Libraries
import os, socket, re, subprocess, time, logging
from datetime import datetime

# Flask
from flask import Flask, render_template, send_from_directory, request

# Flask App
app = Flask(__name__, static_folder="static")

# Logging
logger = logging.getLogger('my_logger') 

file_handler = logging.FileHandler('server.log')
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))  # Assign the formatter to the handler

logger.setLevel(logging.DEBUG)
logger.addHandler(file_handler)

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
    match = re.search(r"^\d{2}\/\d{2}\/\d{4} \d{2}:\d{2}:\d{2}$", string)
    if not match:
        return 'Invalid format', 400
    
    # Log (security)
    logger.info(f"{request.remote_addr} changed the server time from '{datetime.now().strftime('%m/%d/%Y %H:%M:%S')}' to '{string}'")
    
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
        # MacOS (brew install imagesnap)
        os.system(f'imagesnap {app.root_path}/media/pictures/preview.jpg')
    already_taking = False

    return 'Image taken', 200

# Pictures & Archives
folders = ['Pictures', 'Archives', 'Videos']
folders_lowercase = ['pictures', 'archives', 'videos']

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

# Run!
if __name__ == '__main__':
    app.run(debug=(not isRaspberryPi), host="0.0.0.0")