import json
import moviepy as mp
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Load data
with open(PROJECT_ROOT / "data" / "transcripts.json", "r", encoding="utf-8") as f:
    segments = json.load(f)

with open(PROJECT_ROOT / "data" / "emotional_peaks.json", "r", encoding="utf-8") as f:
    peaks = json.load(f)

input_video = PROJECT_ROOT / "data" / "input.mp4"
output_video = PROJECT_ROOT / "outputs" / "video_with_captions.mp4"

clip = mp.VideoFileClip(str(input_video))

highlight_clips = []
caption_clips = []
timeline_map = []

offset = 0

# 🔥 STEP 1: Build clips + timeline mapping
for peak in peaks:
    start = peak["start"]
    end = peak["end"]

    if end <= start:
        continue

    subclip = clip.subclipped(start, end)
    highlight_clips.append(subclip)

    duration = end - start

    timeline_map.append({
        "orig_start": start,
        "orig_end": end,
        "new_start": offset,
        "new_end": offset + duration
    })

    offset += duration

# 🔥 STEP 2: Create highlight video
highlight_video = mp.concatenate_videoclips(highlight_clips)

# 🔥 STEP 3: Add captions using mapping
for mapping in timeline_map:
    orig_start = mapping["orig_start"]
    orig_end = mapping["orig_end"]
    new_start_base = mapping["new_start"]

    for seg in segments:
        if seg["start"] >= orig_start and seg["end"] <= orig_end:

            new_start = new_start_base + (seg["start"] - orig_start)
            new_end = new_start_base + (seg["end"] - orig_start)

            txt_clip = mp.TextClip(
                text=seg["text"],
                font_size=40,
                color="white",
                bg_color="black",
                size=(highlight_video.w, None),
                method="caption"
            ).with_position(("center", "bottom")) \
             .with_start(new_start) \
             .with_end(new_end)

            caption_clips.append(txt_clip)

# 🔥 STEP 4: Overlay captions on highlight video
final = mp.CompositeVideoClip([highlight_video, *caption_clips])
final = final.with_audio(highlight_video.audio)

final.write_videofile(str(output_video), codec="libx264", audio_codec="aac")

# Cleanup
clip.close()
highlight_video.close()
final.close()
for c in caption_clips:
    c.close()

print(f"Saved highlights with captions to {output_video}")