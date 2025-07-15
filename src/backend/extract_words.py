import json
import re
import logging
import os

logging.basicConfig(level=logging.INFO)

def extract_unique_hebrew_words(json_path, output_path):
    unique_words = set()
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        def flatten(data):
            if isinstance(data, dict):
                for value in data.values():
                    yield from flatten(value)
            elif isinstance(data, list):
                for item in data:
                    yield from flatten(item)
            elif isinstance(data, str):
                # Strict clean: Hebrew letters + nikud only (remove punct/cantillation)
                cleaned = re.sub(r'[^\u05D0-\u05EA\u05B0-\u05BC\u05C1-\u05C2\u05C7]', '', data).strip()
                if cleaned:
                    yield cleaned
        for word in flatten(data):
            unique_words.add(word)
        logging.info(f"Extracted {len(unique_words)} unique Hebrew words")
        with open(output_path, 'w', encoding='utf-8') as f:
            for word in sorted(unique_words):
                f.write(f"{word}\n")
    except Exception as e:
        logging.error(f"Error extracting words: {e}")
        raise

extract_unique_hebrew_words('data/text/hebrew_bible_with_nikkud.json', 'data/words.txt')

# Unit test (run to verify)
def test_extract():
    sample = {"Book": [[["אָדָ֥ם", "שֵׁ֖ת", "׃"]]]}
    with open('temp.json', 'w', encoding='utf-8') as f:
        json.dump(sample, f)
    extract_unique_hebrew_words('temp.json', 'temp.txt')
    with open('temp.txt', 'r', encoding='utf-8') as f:
        words = [line.strip() for line in f if line.strip()]  # Robust read
    print(f"Expected words: {['אָדָם', 'שֵׁת']}")
    print(f"Actual words: {words}")
    assert words == ['אָדָם', 'שֵׁת']  # Punct removed
    os.remove('temp.json')
    os.remove('temp.txt')
test_extract()  # No error = pass