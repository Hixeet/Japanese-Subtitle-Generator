import subprocess
import sys
import os
from datetime import datetime

video_path = sys.argv[1]

filename = os.path.splitext(os.path.basename(video_path))[0]

audio_file = f"audio/{filename}.wav"
transcript_file = f"output/{filename}_transcript.json"

python = sys.executable

def log(msg):
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}")

steps = [

    ("Extract Audio", ["script/extract_audio.py", video_path]),

    ("Transcribe (FAST)", ["script/build_transcript.py", audio_file]),

    ("Build Subtitle", ["script/build_subtitle.py", transcript_file]),

    ("Build Furigana", ["script/build_furigana.py", transcript_file])

]

start_time = datetime.now()
log("Starting processing...\n")

for name, cmd in steps:
    log(f"--- {name} ---")
    subprocess.run([python] + cmd)

end_time = datetime.now()

log("Processing finished")
print(f"Total time: {end_time - start_time}")