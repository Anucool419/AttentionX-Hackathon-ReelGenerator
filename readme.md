# 🎬 AI Highlight Reel Generator

Turn long videos into engaging, captioned highlight reels automatically.

This project takes a video as input, detects emotionally significant moments using audio + NLP, extracts those segments, and generates a final short-form video with captions—perfect for reels, shorts, and social media content.

---

## 🚀 Features

* 🎧 **Audio Transcription** using Whisper
* 💬 **Sentiment & Emotion Detection** using Transformers
* 🔊 **Loudness-based Peak Detection** for impactful moments
* ✂️ **Automatic Video Clipping** based on emotional peaks
* 🎞️ **Highlight Reel Generation** (merged clips)
* 📝 **Dynamic Caption Overlay** synced with speech
* ⚡ Fully automated pipeline

---

## 🧠 How It Works

```text
Input Video
    ↓
Audio Extraction
    ↓
Transcription (Whisper)
    ↓
Sentiment + Loudness Analysis
    ↓
Emotion Peak Detection
    ↓
Clip Extraction
    ↓
Timeline Mapping
    ↓
Caption Overlay
    ↓
Final Highlight Reel 🎉
```

---

## 📁 Project Structure

```text
project/
│
├── data/
│   ├── input.mp4
│   ├── audio.wav
│   ├── transcripts.json
│   └── emotional_peaks.json
│
├── outputs/
│   ├── highlight_reel.mp4
│   └── video_with_captions.mp4
│
├── sentiment_analysis.py
├── vision_pipeline.py
├── captions.py
└── README.md
```

---

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/your-username/highlight-reel-ai.git
cd highlight-reel-ai
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Install FFmpeg

Required for video processing:

```bash
# Ubuntu
sudo apt install ffmpeg

# Mac
brew install ffmpeg

# Windows
Download from https://ffmpeg.org/download.html
```

---

## ▶️ Usage

### Step 1: Place your video

```text
data/input.mp4
```

---

### Step 2: Run transcription + emotion detection

```bash
python sentiment_analysis.py
```

Outputs:

* `transcripts.json`
* `emotional_peaks.json`

---

### Step 3: Generate highlight clips

```bash
python vision_pipeline.py
```

Output:

* `highlight_reel.mp4`

---

### Step 4: Add captions

```bash
python captions.py
```

Output:

* `video_with_captions.mp4`

---

## 🧩 Key Concepts

### 🔥 Emotion Peak Detection

Combines:

* Sentiment confidence
* Audio loudness spikes

To identify moments worth clipping.

---

### 🕒 Timeline Mapping (Core Innovation)

After clipping, timestamps no longer match the original video.

This project solves it by mapping:

```text
Original Timeline → Highlight Timeline
```

Ensuring captions stay perfectly synced after merging clips.

---

## 🛠️ Tech Stack

* **Speech Recognition:** Whisper
* **NLP:** Hugging Face Transformers
* **Audio Processing:** Pydub
* **Video Processing:** MoviePy
* **Computer Vision:** YOLOv8 (Ultralytics)
* **Backend:** Python (FASTAPI)
* **Frontend:** Streamlit

---

## ⚠️ Known Issues / Limitations

* Sentiment model is basic (binary classification)
* Emotion detection can be improved with better models
* Caption styling is minimal
* Processing time depends on video length

---

## 🔮 Future Improvements

* 🎯 Advanced emotion models (multi-class emotions)
* 🎨 Animated captions (word-by-word highlights)
* ⚡ Real-time processing pipeline

---

## 💡 Inspiration

Built to simplify content creation for:

* Creators
* Podcasters
* Educators
* Social media marketers

---

## 🎉 Final Output

From a long video → to a short, engaging, captioned highlight reel automatically.

---
## Video link to see demo: https://www.loom.com/share/8c5e97b66efe4537b5de2e5a4ed83a6c

## 🙌 Acknowledgements

* OpenAI Whisper
* Hugging Face
* Ultralytics YOLO
* MoviePy

---
### Live demo: https://attentionx-hackathon-reelgenerator.onrender.com
### ⭐ If you like this project, consider giving it a star!
