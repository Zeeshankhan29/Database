import cv2
import os
import time
from ultralytics import YOLO

output_frames_folder = r'C:\Users\Zeeshan.khan\vscode_projects\research\annotated_frames1'
os.makedirs(output_frames_folder, exist_ok=True)

modelc1 = YOLO(r'C:\Users\Zeeshan.khan\vscode_projects\research\release-SPAR-82-classes-classification-model-256X256-v1.0.0\release-SPAR-82-classes-classification-model-256X256-v1.0.0\release-SPAR-82-classes-classification-model-256X256-v1.0.0\weights\best.pt')
input_video_path = r'C:\Users\Zeeshan.khan\vscode_projects\research\SPAR_data-0_val_output_video_output.mp4'
output_video_path = r'C:\Users\Zeeshan.khan\vscode_projects\research\SPAR_data_output_with_predictions1.mp4'

cap = cv2.VideoCapture(input_video_path)
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = int(cap.get(cv2.CAP_PROP_FPS))

frame_skip = 80  # Skip 9 out of 10 frames to speed up processing
frame_count = 0

while cap.isOpened():
    ret, frame = cap.read()

    if not ret:
        print("End of video.")
        break

    # Skip frames to speed up processing
    if frame_count % frame_skip != 0:
        frame_count += 1
        continue

    # Optional: Resize frame to reduce computation
    frame = cv2.resize(frame, (640, 480))

    results = modelc1(frame)
    detect = []
    
    for result in results:
        if hasattr(result, "probs") and result.probs.top5:
            for value, confd in zip(result.probs.top5, result.probs.top5conf):
                class_name = result.names[value]
                confidence = round(float(confd.numpy()), 2)
                detect.append((class_name, confidence))

    # Sort predictions by confidence and annotate the frame with top predictions
    if detect:
        sorted_detect = sorted(detect, key=lambda x: -x[1])
        # Draw predictions on the frame
        for i, (class_name, conf) in enumerate(sorted_detect[:5]):
            text = f'{class_name}: {conf:.2f}%'
            cv2.putText(frame, text, (10, 30 + i * 20), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 1)

    # Save the annotated frame to the folder
    frame_filename = os.path.join(output_frames_folder, f'frame_{frame_count:04d}.jpg')
    cv2.imwrite(frame_filename, frame)
    
    frame_count += 1

cap.release()
cv2.destroyAllWindows()




import cv2
import os

# Video output path
output_video_path = r'C:\Users\Zeeshan.khan\vscode_projects\research\SPAR_data_output_with_predictions1.mp4'

# Folder containing saved annotated frames
output_frames_folder = r'C:\Users\Zeeshan.khan\vscode_projects\research\annotated_frames1'

# Get list of all the frame files and sort them numerically based on the frame number
frame_files = sorted([f for f in os.listdir(output_frames_folder) if f.endswith('.jpg')],
                     key=lambda x: int(x.split('_')[1].split('.')[0]))  # Sort by frame number

# Ensure the frame size is consistent (width, height) and set the correct fps
first_frame_path = os.path.join(output_frames_folder, frame_files[0])
first_frame = cv2.imread(first_frame_path)
height, width, layers = first_frame.shape
fps = 1 # Set to desired fps (can be adjusted)

# Initialize the video writer
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter(output_video_path, fourcc, fps, (width, height))

# Write each frame to the video
for frame_file in frame_files:
    frame_path = os.path.join(output_frames_folder, frame_file)
    frame = cv2.imread(frame_path)

    if frame is not None:
        out.write(frame)  # Add frame to the video
    else:
        print(f"Skipping {frame_file} due to loading error")

# Release the video writer after writing all frames
out.release()
print(f"Video saved at: {output_video_path}")
