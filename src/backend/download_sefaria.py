import subprocess
import logging
import os
from concurrent.futures import ThreadPoolExecutor
from hashlib import sha256

logging.basicConfig(level=logging.INFO)

tanakh_books = {
    'Torah': ['Genesis', 'Exodus', 'Leviticus', 'Numbers', 'Deuteronomy'],
    'Prophets': ['Joshua', 'Judges', 'I Samuel', 'II Samuel', 'I Kings', 'II Kings', 'Isaiah', 'Jeremiah', 'Ezekiel', 'Hosea', 'Joel', 'Amos', 'Obadiah', 'Jonah', 'Micah', 'Nahum', 'Habakkuk', 'Zephaniah', 'Haggai', 'Zechariah', 'Malachi'],
    'Writings': ['Psalms', 'Proverbs', 'Job', 'Song of Songs', 'Ruth', 'Lamentations', 'Ecclesiastes', 'Esther', 'Daniel', 'Ezra', 'Nehemiah', 'I Chronicles', 'II Chronicles']
}

# Optional hashes (computed from successful downloads; add more as needed)
known_hashes = {
    'Genesis': 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855',  # Example SHA256; replace with actual from your files
    'Exodus': 'your_hash_from_successful_download',  # e.g., hashlib.sha256(open('path').read()).hexdigest()
    'I Samuel': 'your_hash_for_I_Samuel'
    # Add for others if paranoid
}

def download_book(section, book, local_dir, language='Hebrew', version='Tanach with Text Only'):
    book_encoded = book.replace(' ', '%20')
    url = f"https://raw.githubusercontent.com/Sefaria/Sefaria-Export/master/json/Tanakh/{section}/{book_encoded}/{language}/{version.replace(' ', '%20')}.json"
    path = os.path.join(local_dir, 'json', 'Tanakh', section, book, language, f"{version}.json")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    try:
        subprocess.run(["wget", "--tries=3", "-O", path, url], check=True)
        # Hash check if available
        if book in known_hashes:
            with open(path, 'rb') as f:
                file_hash = sha256(f.read()).hexdigest()
            if file_hash != known_hashes[book]:
                raise ValueError(f"Hash mismatch for {book}: got {file_hash}, expected {known_hashes[book]}")
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