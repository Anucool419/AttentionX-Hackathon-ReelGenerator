import whisper
import math
import json
from transformers import pipeline
from pydub import AudioSegment

def process_audio_sentiment():
    #Load whisper model(tiny/medium for speed)
    model=whisper.load_model('small')

    #Transcribe audio
    result=model.transcribe('data/audio.wav')

    #Full transcript
    print(result['text'])

    #Segments with timestamps
    for seg in result["segments"]:
        print(f"{seg['start']}s - {seg['end']}s: {seg['text']}")

    # Save transcript segments to data/transcripts.json
    with open("data/transcripts.json", "w") as f:
        json.dump(result["segments"], f, indent=2)

    ##Using transformers for sentiment scoring
    # Load sentiment pipeline
    sentiment_analyzer = pipeline("text-classification", model="j-hartmann/emotion-english-distilroberta-base")
    
    # Analyze each transcript segment
    emotions = []
    for seg in result["segments"]:
        analysis = sentiment_analyzer(seg["text"])[0]
        emotions.append({
            "start": seg["start"],
            "end": seg["end"],
            "text": seg["text"],
            "label": analysis["label"],
            "score": analysis["score"]
        })

    # Load audio
    audio = AudioSegment.from_wav("data/audio.wav")

    # Split into chunks (e.g., 1s)
    chunk_length_ms = 1000
    loudness = []
    for i in range(0, len(audio), chunk_length_ms):
        chunk = audio[i:i+chunk_length_ms]
        loudness.append(chunk.dBFS)

    # Compute median loudness
    median_loudness = sorted(loudness)[len(loudness)//2]

    # Set threshold slightly above median
    audio_threshold = median_loudness + 5  # threshold slightly above median loudness
    print("Median loudness:", median_loudness, "Threshold:", audio_threshold)
    
    # Mark peaks: loudness above threshold + strong sentiment
    emotional_peaks = []
    for e in emotions:
        # Map transcript timestamps to chunk indices and keep at least one chunk.
        start_idx = max(0, int(math.floor(e["start"])))
        end_idx = min(len(loudness), max(start_idx + 1, int(math.ceil(e["end"]))))
        window = [v for v in loudness[start_idx:end_idx] if v != float("-inf")]

        if not window:
            continue

        avg_loudness = sum(window) / len(window)
        e["avg_loudness"] = avg_loudness

        if avg_loudness > audio_threshold and e["score"] >= 0.6:
            emotional_peaks.append(e)

    # Fallback: if strict filter returns no rows, keep top sentiment segments with valid loudness.
    if not emotional_peaks:
        candidates = [e for e in emotions if "avg_loudness" in e]
        candidates.sort(key=lambda x: x["score"], reverse=True)
        emotional_peaks = candidates[:5]

    for peak in emotional_peaks:
        print(f"Peak {peak['start']}s-{peak['end']}s | {peak['label']} ({peak['score']:.2f}) | {peak['text']}")

    # Save emotional peaks to JSON for vision pipeline
    with open("data/emotional_peaks.json", "w") as f:
        json.dump(emotional_peaks, f, indent=2)

    print("Saved emotional peaks to data/emotional_peaks.json")

if __name__ == "__main__":
    process_audio_sentiment()


    
