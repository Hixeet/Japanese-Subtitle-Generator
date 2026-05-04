import whisperx
import json
import sys
import os
from datetime import datetime

def log(msg):
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}")

audio_file = sys.argv[1]

filename = os.path.splitext(os.path.basename(audio_file))[0]
output_file = f"output/{filename}_aligned.json"

device = "cpu"

os.makedirs("output", exist_ok=True)

log("Loading WhisperX model...")
model = whisperx.load_model("medium", device)

log("Running transcription...")
result = model.transcribe(audio_file)

log("Loading alignment model...")
model_a, metadata = whisperx.load_align_model(
    language_code="ja",
    device=device
)

log("Aligning words...")
aligned_segments = whisperx.align(
    result["segments"],
    model_a,
    metadata,
    audio_file,
    device
)

with open(output_file, "w", encoding="utf8") as f:
    json.dump(aligned_segments, f, ensure_ascii=False, indent=2)

log(f"Alignment saved: {output_file}")