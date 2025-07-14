import json
from phonemizer import phonemize
import os

def generate_lexicon(json_path, lexicon_path):
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            tanakh = json.load(f)  # Assume [{'book':, 'chapter':, 'verse':, 'text':}] or similar; adjust if dict
        words = set()
        for entry in tanakh:
            text = entry['text'].replace('יְהוָה', 'אֲדֹנָי').replace('-', '').replace('׃', '')  # Sites' prep, secure replace
            words.update(text.split())
        # Batch phonemize (scalable, offline)
        phonemes = phonemize(list(words), language='he', backend='espeak', strip=True)
        with open(lexicon_path, 'w', encoding='utf-8') as f:
            for word, phon in zip(sorted(words), phonemes):
                f.write(f"{word} {phon.upper().replace(' ', '')}\n")  # MFA format
    except Exception as e:
        print(f"Error generating lexicon: {e}")  # Logging for DevOps

generate_lexicon('data/text/hebrew_bible_with_nikkud.json', 'data/lexicon.dict')