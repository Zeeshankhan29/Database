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
from ultralytics import YOLO
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
qr_cam_indices = value1.qr_camera_no
img_cam_indices = value1.img_camera_no

#Qr indices Camera Object
qr_cam_predict = [(idx,cv2.VideoCapture(idx)) for idx in qr_cam_indices]

#Image indices Camera Object
img_cam_predict = [(idx1,cv2.VideoCapture(idx1)) for idx1 in img_cam_indices]

# Create a QReader instance
qreader = QReader()
lock = threading.Lock()


def pass_img(files):
    stream_file = Image.open(files.stream)
    arr = np.array(stream_file)
    rgb_img = cv2.cvtColor(arr, cv2.COLOR_BGR2RGB)
    return rgb_img

def img_prediction(camera,index,lock):
    ret, frame = camera.read()
    model = YOLO('models/best.pt')
    os.makedirs('image_prediction',exist_ok =True)
    filename = os.path.join(os.getcwd(),'image_prediction',f'capture_{index}_{time.time()}.png') 
    store = cv2.imwrite(filename,frame)
    result = model(filename,save=True,imgsz=640,conf=0.9)
    return result,f"camera_index :{index}" 

def process_camera(camera,index,lock):
    ret,img = camera.read()
    os.makedirs('capture',exist_ok=True)
    filename = os.path.join(os.getcwd(),'capture',f'capture_{index}_{time.time()}.png') 
    store = cv2.imwrite(filename,img)
    logging.info(f'file {filename} saved.')
    decoded_text = qreader.detect_and_decode(image=img)
    logging.info(f'Camera {camera} - Data detected: {decoded_text}')
    return decoded_text,f"Image_captured : {store}", f"camera_index : {index}"

@app.route('/QRdetect', methods=['POST'])
def qrdetection():
    # Use threading to process cameras concurrently
    threads = []
    results = []
    global lock
    global qr_cam_predict 

    for idx, camera in enumerate(qr_cam_predict):
        thread = threading.Thread(target=lambda i=idx: results.append(process_camera(qr_cam_predict[i][1],qr_cam_predict[i][0],lock)))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    return jsonify(results)

@app.route('/IMgdetect', methods=['POST'])
def imgdetection():
    # Use threading to process cameras concurrently
    threads = []
    results = []
    global lock
    global img_cam_indices

    for idx, camera in enumerate(img_cam_predict):
        thread = threading.Thread(target=lambda i=idx: results.append(img_prediction(img_cam_predict[i][1],img_cam_predict[i][0],lock)))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    return jsonify(results)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=500)
