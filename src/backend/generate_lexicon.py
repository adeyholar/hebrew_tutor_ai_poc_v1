import json
from phonikud import phonemize, normalize
import os
import logging

logging.basicConfig(level=logging.INFO)

def flatten_texts(data):
    """Generator to flatten nested dict texts (modular, memory-efficient)."""
    if isinstance(data, dict):
        for value in data.values():
            yield from flatten_texts(value)
    elif isinstance(data, str):
        yield data

def generate_lexicon(json_path, lexicon_path):
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            tanakh = json.load(f)
        words = set()
        for text in flatten_texts(tanakh):
            cleaned = text.replace('יְהוָה', 'אֲדֹנָי').replace('-', '').replace('׃', '')  # Secure cleaning
            words.update(cleaned.split())
        logging.info(f"Extracted {len(words)} unique words")
        with open(lexicon_path, 'w', encoding='utf-8') as f:
            for word in sorted(words):
                norm_word = normalize(word)  # Handle nikud consistency
                phon = phonemize(norm_word)
                f.write(f"{word} {phon.upper().replace(' ', '')}\n")
    except Exception as e:
        logging.error(f"Error generating lexicon: {e}")
        raise

generate_lexicon('data/text/hebrew_bible_with_nikkud.json', 'data/lexicon.dict')