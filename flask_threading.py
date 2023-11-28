from flask import Flask, jsonify
import os
import cv2
import threading
import time


app = Flask(__name__)

camera_index = [0,1]
camera_obj = [cv2.VideoCapture(idx) for idx in camera_index]
lock = threading.Lock()

results = []
def process(camera,index,lock):
    ret , frame = camera.read()
    if not ret :
        print(f'Error reading data from camera {index}')

    if frame.size == 0 or frame is None:
        print(f'No Image found in camera {index}')

    os.makedirs('data',exist_ok=True)
    filename = f'data/capture_{index}_{time.time()}.png'
    cv2.imwrite(filename,frame)

    if lock:
        results.append(f"{filename} captured with camera {index}")


@app.route('/pred', methods=['POST'])
def caphold():
    threads = []
    global camera_index
    global camera_obj
    global lock
    
    for index,camera_obj_value in enumerate(camera_obj):
        thread = threading.Thread(target=process, args=(camera_obj_value,index,lock))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    return jsonify('results captured with all camera successfully')


if __name__ == '__main__':
    app.run(debug=True)

