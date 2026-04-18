import cv2 as cv
import shutil
from pathlib import Path
from ultralytics import YOLO
import moviepy as mp
from moviepy import concatenate_videoclips, VideoFileClip

# Load YOLO model (nano for speed)
PROJECT_ROOT = Path(__file__).resolve().parent.parent
MODEL_PATH = PROJECT_ROOT / "yolov8n.pt"

if MODEL_PATH.exists():
    model = YOLO(str(MODEL_PATH))
else:
    print(f"Model not found at {MODEL_PATH}. Downloading once...")
    downloaded_model = YOLO("yolov8n.pt")

    # Persist downloaded weights at project root so future runs reuse one location.
    ckpt_path = Path(downloaded_model.ckpt_path) if getattr(downloaded_model, "ckpt_path", None) else None
    if ckpt_path and ckpt_path.exists() and ckpt_path.resolve() != MODEL_PATH.resolve():
        shutil.copy2(ckpt_path, MODEL_PATH)
        model = YOLO(str(MODEL_PATH))
    else:
        model = downloaded_model

# Input and output paths
input_video = "data/input.mp4"
#output_video = "outputs/cropped_vertical.mp4"
output_video = "outputs/highlight_reel.mp4"
import json
# Load emotional peaks from sentiment_analysis
with open("data/emotional_peaks.json", "r") as f:
    peaks = json.load(f)   # each peak has start, end timestamps

cap = cv.VideoCapture(input_video)
fps = int(cap.get(cv.CAP_PROP_FPS))
width = int(cap.get(cv.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv.CAP_PROP_FRAME_HEIGHT))

# Define vertical crop size (9:16)
target_width = int(height * 9 / 16)
target_height = height

fourcc = cv.VideoWriter_fourcc(*"mp4v")
out = cv.VideoWriter(output_video, fourcc, fps, (target_width, target_height))



clip = VideoFileClip(input_video)

# Collect highlight subclips (with audio preserved)
highlight_clips = []
for peak in peaks:
    start = peak["start"]
    end = peak["end"]
    
    
    # Guard against invalid ranges
    if end <= start:
        print(f"Skipping invalid peak: start={start}, end={end}")
        continue

    # Clamp to video duration
    if start < 0:
        start = 0
    if end > clip.duration:
        end = clip.duration

    # Only add if there's at least 0.5s of video
    if end - start >= 0.5:
        subclip = clip.subclip(start, end)
        highlight_clips.append(subclip)
    else:
        print(f"Skipping too-short peak: start={start}, end={end}")
    
    # Guard: only process valid ranges
    if end > start and end <= clip.duration:
        subclip = clip.subclipped(start, end)
        highlight_clips.append(subclip)
    else:
        print(f"Skipping invalid peak: start={start}, end={end}")
if highlight_clips:
    final = concatenate_videoclips(highlight_clips)
    final.write_videofile("outputs/highlight_reel.mp4", codec="libx264", audio_codec="aac")
print(f"Saved highlight video to {output_video}")

# final = concatenate_videoclips(highlight_clips)
# final.write_videofile(output_video, codec="libx264", audio_codec="aac")
# for peak in peaks:
#     start_frame = int(peak["start"] * fps)
#     end_frame = int(peak["end"] * fps)

#     cap.set(cv.CAP_PROP_POS_FRAMES, start_frame)

#     for frame_idx in range(start_frame, end_frame):
#         ret, frame = cap.read()
#         if not ret:
#             break

#         # Run YOLO inference
#         results = model(frame, verbose=False)
#         crop_center_x = width // 2

#         for r in results:
#             for box in r.boxes:
#                 cls = int(box.cls[0])
#                 label = model.names[cls]
#                 if label == "person":  # YOLO detects 'person'
#                     x1, y1, x2, y2 = box.xyxy[0].int().tolist()
#                     crop_center_x = (x1 + x2) // 2
#                     break

#         # Compute crop boundaries
#         left = max(0, crop_center_x - target_width // 2)
#         right = min(width, crop_center_x + target_width // 2)

#         cropped_frame = frame[:, left:right]
#         cropped_frame = cv.resize(cropped_frame, (target_width, target_height))

#         out.write(cropped_frame)

# cap.release()
# out.release()
# cv.destroyAllWindows()





