import os
import socket

from flask import Flask, render_template, send_file

app = Flask(__name__)

hostname = socket.gethostname()


@app.route('/')
def index():
    return render_template('index.html', hostname=hostname)

video_file = '/home/pi/timelapse/media/videos/timelapse.webm'
@app.route('/video')
def video():
    if not os.path.exists(video_file):
        return bytes('Error: ' +video_file + ' does not exist... :(', 'utf-8')
    return send_file('/home/pi/timelapse/media/videos/timelapse.webm')
    # with open('/home/pi/timelapse/media/videos/timelapse.webm', 'r') as file:
    #     return file.read()

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")