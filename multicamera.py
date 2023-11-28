import os
import re
import logging
from flask import Flask, jsonify, request
from qreader import QReader
import numpy as np
import time
import warnings
from box import ConfigBox
import yaml
from PIL import Image
import cv2
import threading

app = Flask(__name__)

# log directory
log_path = 'predict.log'

# Set up logging
log_format = '[%(asctime)s] : [%(name)s] : [%(levelname)s] :[%(message)s]'
logging.basicConfig(filename=log_path, level=logging.DEBUG, format=log_format)
stream = logging.StreamHandler()
log = logging.getLogger()
log.addHandler(stream)

#Load your yaml file
with open('config.yaml','r') as conf:
    value = yaml.safe_load(conf) or {}
    value1 = ConfigBox(value)


# Initialize the cameras
# Use appropriate camera indices based on your system configuration
camera_indices = value1.camera_no
cameras = [cv2.VideoCapture(idx) for idx in camera_indices]

# Create a QReader instance
qreader = QReader()


def pass_img(files):
    stream_file = Image.open(files.stream)
    arr = np.array(stream_file)
    rgb_img = cv2.cvtColor(arr, cv2.COLOR_BGR2RGB)
    return rgb_img

def process_camera(camera):
    ret,img = camera.read()
    decoded_text = qreader.detect_and_decode(image=img)
    logging.info(f'Camera {camera} - Data detected: {decoded_text}')
    return decoded_text

@app.route('/QRdetect', methods=['POST'])
def detection():
    # Use threading to process cameras concurrently
    threads = []
    results = []

    for idx, camera in enumerate(cameras):
        thread = threading.Thread(target=lambda i=idx: results.append(process_camera(cameras[i])))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    return jsonify(results)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=500)




















import os
import re
import logging
from flask import Flask, jsonify, request
from qreader import QReader
import numpy as np
import time
import warnings
from box import ConfigBox
import yaml
from PIL import Image
import cv2
import threading

app = Flask(__name__)

# log directory
log_path = 'predict.log'

# Set up logging
log_format = '[%(asctime)s] : [%(name)s] : [%(levelname)s] :[%(message)s]'
logging.basicConfig(filename=log_path, level=logging.DEBUG, format=log_format)
stream = logging.StreamHandler()
log = logging.getLogger()
log.addHandler(stream)

# Load the YOLO model
# Not implemented in the provided snippet

# Initialize the cameras
# Use appropriate camera indices based on your system configuration
qr_camera_indices = [0, 1, 2]
image_camera_indices = [3, 4, 5]

qr_cameras = [cv2.VideoCapture(idx) for idx in qr_camera_indices]
image_cameras = [cv2.VideoCapture(idx) for idx in image_camera_indices]

# Create a QReader instance for QR code prediction
qreader_qr = QReader()

def capture_image(camera):
    ret, frame = camera.read()
    return frame

def pass_img(files):
    stream_file = Image.open(files.stream)
    arr = np.array(stream_file)
    rgb_img = cv2.cvtColor(arr, cv2.COLOR_BGR2RGB)
    return rgb_img

def process_qr_camera(camera):
    img = capture_image(camera)
    decoded_text = qreader_qr.detect_and_decode(image=img)
    logging.info(f'QR Camera {camera} - Data detected: {decoded_text}')
    return decoded_text

def process_image_camera(camera):
    img = capture_image(camera)
    # Implement image prediction logic here
    # Example: result = predict_image(img)
    result = "Image prediction result"
    logging.info(f'Image Camera {camera} - Prediction: {result}')
    return result

@app.route('/predictQR', methods=['POST'])
def predict_qr():
    # Use threading to process QR cameras concurrently
    threads = []
    results = []

    for idx, camera in enumerate(qr_cameras):
        thread = threading.Thread(target=lambda i=idx: results.append(process_qr_camera(qr_cameras[i])))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    return jsonify(results)

@app.route('/predictImage', methods=['POST'])
def predict_image():
    # Use threading to process image cameras concurrently
    threads = []
    results = []

    for idx, camera in enumerate(image_cameras):
        thread = threading.Thread(target=lambda i=idx: results.append(process_image_camera(image_cameras[i])))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    return jsonify(results)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=500)



#please see below
    |
    |
    |
    |
    |
    |
    |
    |
  __|
\|/































#flask server
from flask import Flask, jsonify
import os
import cv2
import threading
import time

app = Flask(__name__)

def capture(camera, lock, index):
    ret, frame = camera.read()

    if not ret:
        print(f'Error in camera {index} while capturing')

    if frame is None or frame.size == 0:
        print(f'Image not valid captured from camera {index}')

    os.makedirs('data', exist_ok=True)
    filename = f'captured_{index}_{time.time()}.jpg'
    cv2.imwrite(filename, frame)

    with lock:
        results.append(f'{filename} captured ')
    print(results)

@app.route('/capture_images', methods=['POST'])
def capture_images():
    threads = []
    results = []
    for index, camera_obj_value in enumerate(camera_obj):
        thread = threading.Thread(target=capture, args=(camera_obj_value, lock, index))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    return jsonify({'message': 'All results captured'})

if __name__ == '__main__':
    camera_index = [0, 1]
    camera_obj = [cv2.VideoCapture(idx) for idx in camera_index]
    results = []
    lock = threading.Lock()

    app.run(debug=True)

