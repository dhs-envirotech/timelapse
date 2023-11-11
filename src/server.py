import os
import socket

from flask import Flask, render_template, send_file, send_from_directory

app = Flask(__name__, static_folder="static")
hostname = socket.gethostname().replace('.local', '')

pictures = app.root_path + '/media/pictures/'
print(pictures)

# Homepage
@app.route('/')
def index():
    return render_template('index.html', hostname=hostname, names=os.listdir(pictures))

# Hidden
@app.route('/date')
def date():
    return send_file('templates/date.html')

# Picture
@app.route('/picture/<path:name>')
def picture(name):
    return send_from_directory(pictures, name)
 
# Video
video_file = app.root_path + '/media/videos/timelapse.webm'
@app.route('/video')
def video():
    if not os.path.exists(video_file):
        return bytes('Error: ' + video_file + ' does not exist... :(<br><br><a href="/">Go back</a>', 'utf-8')
    return send_file(video_file, mimetype="video/webm")

# Run!
if __name__ == '__main__':
    app.run(debug=('pi' in hostname), host="0.0.0.0")