import ffmpeg
import sys
import os
from datetime import datetime

def log(msg):
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}")

video_path = sys.argv[1]

filename = os.path.splitext(os.path.basename(video_path))[0]
audio_path = f"audio/{filename}.wav"

os.makedirs("audio", exist_ok=True)

log("Extracting audio...")

(
    ffmpeg
    .input(video_path)
    .output(audio_path, ac=1, ar=16000)
    .run()
)

log(f"Audio extracted: {audio_path}")