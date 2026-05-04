import json
import MeCab
import sys
import os
from tqdm import tqdm
from datetime import datetime

def log(msg):
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}")

input_file = sys.argv[1]

filename = os.path.basename(input_file).replace("_transcript.json", "")
output_file = f"output/{filename}_subtitle.json"

tagger = MeCab.Tagger()

with open(input_file, encoding="utf8") as f:
    data = json.load(f)

subtitle = []

log("Building subtitle...")

for seg in tqdm(data, desc="Subtitle"):

    sentence = seg["text"]

    words = []

    node = tagger.parseToNode(sentence)

    while node:
        if node.surface:
            words.append({
                "word": node.surface
            })
        node = node.next

    spaced_sentence = " ".join([w["word"] for w in words])

    subtitle.append({
        "start": seg["start"],
        "end": seg["end"],
        "sentence": sentence,
        "spaced": spaced_sentence,
        "words": words
    })

with open(output_file, "w", encoding="utf8") as f:
    json.dump(subtitle, f, ensure_ascii=False, indent=2)

log(f"Subtitle saved: {output_file}")