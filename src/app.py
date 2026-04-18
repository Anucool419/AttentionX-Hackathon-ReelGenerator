import streamlit as st
import requests

BACKEND_URL = "http://127.0.0.1:8000"

st.title("Highlight Reel Generator 🎬")

st.write("Upload a video and the app will generate transcripts, peaks, and the final reel automatically.")

# Upload video only
video_file = st.file_uploader("Upload your video", type=["mp4"])

if st.button("Submit to Backend"):
    if video_file:
        files = {"file": video_file}
        response = requests.post(f"{BACKEND_URL}/upload", files=files)
        if response.status_code == 200:
            st.success("Upload successful!")
            st.json(response.json())
            download_url = f"{BACKEND_URL}/download/video_with_captions.mp4"
            st.markdown(f"[Download processed video]({download_url})")

        else:
            st.error("Upload failed")
    else:
        st.warning("Please provide a video")
