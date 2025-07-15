import subprocess
import logging
import os
from concurrent.futures import ThreadPoolExecutor
from hashlib import sha256

logging.basicConfig(level=logging.INFO)

tanakh_books = {
    'Torah': ['Genesis', 'Exodus', 'Leviticus', 'Numbers', 'Deuteronomy'],
    'Prophets': ['Joshua', 'Judges', '1 Samuel', '2 Samuel', '1 Kings', '2 Kings', 'Isaiah', 'Jeremiah', 'Ezekiel', 'Hosea', 'Joel', 'Amos', 'Obadiah', 'Jonah', 'Micah', 'Nahum', 'Habakkuk', 'Zephaniah', 'Haggai', 'Zechariah', 'Malachi'],
    'Writings': ['Psalms', 'Proverbs', 'Job', 'Song of Songs', 'Ruth', 'Lamentations', 'Ecclesiastes', 'Esther', 'Daniel', 'Ezra', 'Nehemiah', '1 Chronicles', '2 Chronicles']
}

def download_book(section, book, local_dir, language='Hebrew', version='Tanach with Text Only'):
    book_encoded = book.replace(' ', '%20')
    url = f"https://raw.githubusercontent.com/Sefaria/Sefaria-Export/master/json/Tanakh/{section}/{book}/{language}/{version}.json"
    path = os.path.join(local_dir, 'json', 'Tanakh', section, book, language, f"{version}.json")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    try:
        subprocess.run(["wget", "--tries=3", "-O", path, url], check=True)
        # Optional hash check (example for Genesis; add more)
        if book == 'Genesis':
            with open(path, 'rb') as f:
                file_hash = sha256(f.read()).hexdigest()
            expected = 'your_known_hash_here'  # Compute once: python -c "import hashlib; print(hashlib.sha256(open('file').read()).hexdigest())"
            if file_hash != expected:
                raise ValueError("Hash mismatch for Genesis")
        logging.info(f"Downloaded {book} ({language}/{version})")
    except subprocess.CalledProcessError as e:
        logging.error(f"Failed {book}: {e}")
        raise

def download_sefaria(local_dir):
    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = []
        for section, books in tanakh_books.items():
            for book in books:
                futures.append(executor.submit(download_book, section, book, local_dir))
        for future in futures:
            future.result()

download_sefaria("data/sefaria-export")