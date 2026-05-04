from faster_whisper import WhisperModel
import json
import sys
import os
from datetime import datetime
from tqdm import tqdm

def log(msg):
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}")

audio_path = sys.argv[1]

filename = os.path.splitext(os.path.basename(audio_path))[0]
output_file = f"output/{filename}_transcript.json"

os.makedirs("output", exist_ok=True)

log("Loading Whisper model...")

model = WhisperModel(
    "small",              # 🔥 lebih cepat dari medium
    compute_type="int8"
)

log("Transcribing audio...")

segments, _ = model.transcribe(
    audio_path,
    language="ja",        # 🔥 skip auto detect (lebih cepat)
    word_timestamps=False
)

result = []

segments = list(segments)

for seg in tqdm(segments, desc="Transcript"):
    result.append({
        "start": seg.start,
        "end": seg.end,
        "text": seg.text.strip()
    })

with open(output_file, "w", encoding="utf8") as f:
    json.dump(result, f, ensure_ascii=False, indent=2)

log(f"Transcript saved: {output_file}")