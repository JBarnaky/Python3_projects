import time
import logging
import numpy as np
import cv2
from enum import Enum
from flask import Flask, Response, request, abort
import mss
from mss.exception import ScreenShotError

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Configuration
class ImageFormat(Enum):
    JPEG = "image/jpeg"

MONITOR_INDEX = 0  # Change this if you want to stream a different monitor
FRAMES_PER_SECOND = 60
QUALITY = 75  # 80-100 is good range for JPEG quality
RESIZE = 0.75
DEBUG = False

app = Flask(__name__)
app.config['DEBUG'] = DEBUG

def get_local_ip():
    """Get the local IP address of the machine."""
    try:
        from socket import gethostbyname, gethostname
        return gethostbyname(gethostname())
    except Exception as e:
        logger.error(f"Failed to get local IP: {str(e)}")
        return "127.0.0.1"

def validate_request():
    """Validate incoming requests."""
    if request.method != 'GET' or not request.headers.get('Host'):
        abort(400, 'Invalid request type')

def capture_frame(sct, monitor):
    """Capture a frame from the screen."""
    try:
        screenshot = sct.grab(monitor)
        return np.array(screenshot)
    except ScreenShotError as e:
        logger.error(f"Screen capture error: {str(e)}")
        return None

def process_frame(frame, resize, quality):
    """Process a frame by resizing and encoding it as JPEG."""
    if frame is None:
        return None

    # Resize the frame if necessary
    if resize != 1:
        frame = cv2.resize(frame, (0, 0), fx=resize, fy=resize, interpolation=cv2.INTER_LANCZOS4)

    # Convert to BGR and encode as JPEG
    success, buffer = cv2.imencode('.jpg', cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR), [int(cv2.IMWRITE_JPEG_QUALITY), quality])
    if not success:
        logger.error("Failed to encode image to JPEG")
        return None

    return buffer.tobytes()

def generate_frames():
    """Generate screen frames for streaming."""
    with mss.mss() as sct:
        monitor = sct.monitors[MONITOR_INDEX]
        while True:
            start_time = time.time()
            frame = capture_frame(sct, monitor)
            processed_frame = process_frame(frame, RESIZE, QUALITY)

            if processed_frame is not None:
                yield (
                    b'--frame\r\n'
                    b'Content-Type: ' + ImageFormat.JPEG.value.encode() + b'\r\n\r\n' +
                    processed_frame + b'\r\n'
                )

            processing_time = time.time() - start_time
            sleep_time = max(0.0, 1 / FRAMES_PER_SECOND - processing_time)
            if sleep_time > 0:
                time.sleep(sleep_time)
            else:
                logger.warning(
                    f"Frame processing took longer than expected: {processing_time:.2f}s"
                )

@app.route('/video_feed')
def video_feed():
    validate_request()
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/')
def index():
    """Return the HTML page to display the stream."""
    return """<html>
    <head>
        <title>Screen Stream</title>
    </head>
    <body>
        <h1>Screen Streaming</h1>
        <img src="/video_feed" alt="Screen Stream">
    </body>
</html>"""

def start_server(host='0.0.0.0', port=5000):
    """Start the Flask server."""
    try:
        app.run(host=host, port=port, debug=DEBUG)
    except Exception as e:
        logger.error(f"Failed to start server: {str(e)}")

if __name__ == '__main__':
    local_ip = get_local_ip()
    logger.info(f"Server is available at http://{local_ip}:5000")
    start_server()
