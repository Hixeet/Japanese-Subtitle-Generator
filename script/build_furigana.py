import json
import sys
import os
from fugashi import Tagger
from tqdm import tqdm
from datetime import datetime

def log(msg):
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}")

# 🔥 TAMBAHAN: konversi katakana → hiragana
def katakana_to_hiragana(text):
    result = ""
    for ch in text:
        code = ord(ch)
        # range katakana → hiragana
        if 0x30A1 <= code <= 0x30F6:
            result += chr(code - 0x60)
        else:
            result += ch
    return result


input_file = sys.argv[1]

filename = os.path.basename(input_file).replace("_transcript.json", "")
output_file = f"output/{filename}_furigana.json"

tagger = Tagger()

with open(input_file, encoding="utf8") as f:
    data = json.load(f)

words = []

log("Generating furigana...")

for seg in tqdm(data, desc="Furigana"):

    text = seg["text"]

    for token in tagger(text):

        surface = token.surface
        kana = token.feature.kana

        if kana:
            hira = katakana_to_hiragana(kana)  # 🔥 DIUBAH DI SINI
        else:
            hira = surface

        words.append({
            "word": surface,
            "reading": hira,
            "start": seg["start"],
            "end": seg["end"]
        })

with open(output_file, "w", encoding="utf8") as f:
    json.dump({"words": words}, f, ensure_ascii=False, indent=2)

log(f"Furigana saved: {output_file}")