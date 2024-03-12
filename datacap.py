import cv2
import time
import os
from pathlib import Path
import uuid
import gradio as gr

vid = cv2.VideoCapture(0)
def capture_video_and_images(video_duration, item_name, fps):
  """
  Captures video and images from webcam at a specified FPS.

  Args:
      video_duration: Duration of video capture in seconds.
      item_name: Name of the item being captured.
      fps: Desired frames per second.

  Returns:
      Success message as a string.
  """
  global vid
  # Create output folders
  video_folder = 'item_videos'
  os.makedirs(video_folder, exist_ok=True)
  video_path = os.path.join(video_folder, item_name)
  os.makedirs(video_path, exist_ok=True)

  item_frames = 'item_images'
  os.makedirs(item_frames, exist_ok=True)
  item_path = os.path.join(item_frames, item_name)
  os.makedirs(item_path, exist_ok=True)

  # Initialize video writer
  save_name = os.path.join(video_path, f"{item_name}_{str(uuid.uuid4())}.mp4")
  
  width = int(vid.get(cv2.CAP_PROP_FRAME_WIDTH))
  height = int(vid.get(cv2.CAP_PROP_FRAME_HEIGHT))
  output_size = (width, height)
  out = cv2.VideoWriter(save_name, cv2.VideoWriter_fourcc(*'mp4v'), fps, output_size)

  # Calculate delay between frames (in milliseconds)
  delay = int(1000 / fps)  # 1000 milliseconds per second

  # Capture frames for video duration
  start_time = time.time()
  while time.time() - start_time < video_duration:
    ret, frame = vid.read()
    if ret:
      cv2.imwrite(os.path.join(item_path, f"{item_name}_{str(uuid.uuid4())}.png"), frame)
      out.write(frame)
      # Wait for delay to maintain desired FPS
      time.sleep(delay / 1000)  # Convert milliseconds to seconds
    else:
      break

  # Release resources
  # vid.release()
  out.release()
  # cv2.destroyAllWindows()

  return f"Video and images captured successfully!"


if __name__ == "__main__":
    # Gradio interface definition
    interface = gr.Interface(
    fn=capture_video_and_images,
    inputs=[
        gr.Slider(minimum=1, maximum=30, label="Video Duration (seconds)"),
        gr.Textbox(label="Item Name"),
        gr.Slider(minimum=1, maximum=120, label="FPS"),
    ],
    outputs="text",
    title="Capture Video and Images",
    description="Enter video duration, item name, and desired FPS",
    )

    # Launch the Gradio interface
    interface.launch()
