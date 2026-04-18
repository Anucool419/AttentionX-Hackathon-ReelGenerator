from fastapi import FastAPI, UploadFile
from fastapi.responses import JSONResponse, FileResponse
import json
import subprocess
import sys
from pathlib import Path

app = FastAPI()

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"
OUTPUT_DIR = PROJECT_ROOT / "outputs"
DATA_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

@app.post("/upload")
async def upload_video(file: UploadFile):
    """
    Accepts a video file, saves it to data/input.mp4, then runs the pipeline.
    """
    video_path = DATA_DIR / "input.mp4"
    with open(video_path, "wb") as f:
        f.write(await file.read())

    # Run the processing pipeline from the project root.
    subprocess.run([sys.executable, str(PROJECT_ROOT / "src" / "audio_pipeline.py")], cwd=PROJECT_ROOT, check=True)
    subprocess.run([sys.executable, str(PROJECT_ROOT / "src" / "sentiment_analysis.py")], cwd=PROJECT_ROOT, check=True)
    subprocess.run([sys.executable, str(PROJECT_ROOT / "src" / "captions.py")], cwd=PROJECT_ROOT, check=True)

    return JSONResponse({
        "message": "Upload successful and processing complete",
        "video": file.filename,
        "output": "video_with_captions.mp4"
    })

@app.get("/download/{filename}")
async def download_video(filename: str):
    video_path = PROJECT_ROOT / "outputs" / filename
    if video_path.exists():
        return FileResponse(video_path, media_type="video/mp4", filename=filename)
    return JSONResponse({"error": "File not found"}, status_code=404)
