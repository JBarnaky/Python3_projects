import asyncio
import time
import logging
import numpy as np
import cv2
from enum import Enum
import mss
from mss.exception import ScreenShotError
from aiohttp import web

# Configure logging
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

app = web.Application()
app['DEBUG'] = DEBUG

def get_local_ip():
    """Get the local IP address of the machine."""
    from socket import gethostbyname, gethostname
    try:
        return gethostbyname(gethostname())
    except Exception as e:
        logger.error(f"Failed to get local IP: {str(e)}")
        return "127.0.0.1"

def capture_frame(sct, monitor):
    """Capture a frame from the screen."""
    try:
        screenshot = sct.grab(monitor)
        return np.array(screenshot)
    except ScreenShotError as e:
        logger.error(f"Screen capture error: {str(e)}")
        return None

def process_frame(frame):
    """Process a frame by resizing and encoding it as JPEG."""
    if frame is None:
        return None

    # Resize frame if necessary
    if RESIZE != 1:
        frame = cv2.resize(frame, (int(frame.shape[1] * RESIZE), int(frame.shape[0] * RESIZE)), interpolation=cv2.INTER_LANCZOS4)

    # Encode frame to JPEG
    success, buffer = cv2.imencode('.jpg', cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR), [int(cv2.IMWRITE_JPEG_QUALITY), QUALITY])
    if not success:
        logger.error("Failed to encode image to JPEG")
        return None

    return buffer.tobytes()

async def generate_frames():
    """Generate screen frames for streaming."""
    with mss.mss() as sct:
        monitor = sct.monitors[MONITOR_INDEX]
        while True:
            start_time = time.time()
            frame = capture_frame(sct, monitor)
            processed_frame = process_frame(frame)

            if processed_frame is not None:
                yield (
                    b'--frame\r\n'
                    b'Content-Type: ' + ImageFormat.JPEG.value.encode() + b'\r\n\r\n' +
                    processed_frame + b'\r\n'
                )

            processing_time = time.time() - start_time
            sleep_time = max(0.0, 1 / FRAMES_PER_SECOND - processing_time)
            if sleep_time > 0:
                await asyncio.sleep(sleep_time)
            else:
                logger.warning(f"Frame processing took longer than expected: {processing_time:.2f}s")

async def video_feed(request):
    """Stream video feed."""
    response = web.StreamResponse(status=200, reason='OK')
    response.headers['Content-Type'] = 'multipart/x-mixed-replace; boundary=frame'
    await response.prepare(request)

    async for frame in generate_frames():
        await response.write(frame)

    return response

async def index(request):
    """Return the HTML page to display the stream."""
    return web.Response(text="""<html>
    <head>
        <title>Screen Stream</title>
    </head>
    <body>
        <h1>Screen Streaming</h1>
        <img src="/video_feed" alt="Screen Stream">
    </body>
</html>""", content_type='text/html')

def start_server(host='0.0.0.0', port=5000):
    """Start the aiohttp server."""
    app.router.add_get('/video_feed', video_feed)
    app.router.add_get('/', index)

    web.run_app(app, host=host, port=port)

if __name__ == '__main__':
    local_ip = get_local_ip()
    logger.info(f"Server is available at http://{local_ip}:5000")
    start_server()