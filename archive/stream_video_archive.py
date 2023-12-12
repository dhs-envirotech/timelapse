# CODE ARCHIVE

# Live Preview
class LiveStream:
    def __init__(self):
        self.stream = None
        self.camera = None

    def new_stream(self):
        while True:
            success, frame = self.camera.read()
            if not success:
                break
            else:
                ret, buffer = cv2.imencode('.jpg', frame)

                frame = buffer.tobytes()
                yield (b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    def start(self):
        if self.camera is None:
            self.camera = cv2.VideoCapture(0)
        if self.stream is None:
            self.stream = self.new_stream()
        return self.stream

    def stop(self):
        self.stream = None
        if self.camera is not None:
            self.camera.release()
        self.camera = None
        time.sleep(1)

camera_reservation_file = app.root_path + '/camera_reserved.txt'
live_stream  = LiveStream()
@app.route('/live')
def video_feed():
    if not os.path.exists(camera_reservation_file):
        return Response(live_stream.start(), mimetype='multipart/x-mixed-replace; boundary=frame')
    return 'Camera Reserved', 404

@app.after_request
def after_request(response):
    global streaming, stream
    if request.path == '/video_feed':
       live_stream.stop()
    return response