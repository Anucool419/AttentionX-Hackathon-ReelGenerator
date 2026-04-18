from pathlib import Path
from moviepy import VideoFileClip

PROJECT_ROOT = Path(__file__).resolve().parent.parent
INPUT_VIDEO = PROJECT_ROOT / "data" / "input.mp4"
OUTPUT_AUDIO = PROJECT_ROOT / "data" / "audio.wav"

if not INPUT_VIDEO.exists():
	raise FileNotFoundError(f"Input video not found: {INPUT_VIDEO}")

with VideoFileClip(str(INPUT_VIDEO)) as video:
	if video.audio is None:
		raise ValueError("Input video has no audio track")
	video.audio.write_audiofile(str(OUTPUT_AUDIO))

