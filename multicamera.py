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
