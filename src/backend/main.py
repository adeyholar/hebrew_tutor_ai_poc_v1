# src/backend/main.py
from fastapi import FastAPI, Query
from fastapi.responses import FileResponse
from gtts import gTTS
import os
import pickle
from pydantic import BaseModel
import tempfile

app = FastAPI()

# Load lexicon (secure: read-only)
with open('../data/lexicon.dict', 'rb') as f:  # Adjust path
    lexicon = pickle.load(f)

class TTSRequest(BaseModel):
    text: str
    speed: float = 1.0

@app.post("/tts")
async def generate_tts(request: TTSRequest):
    # Validate input
    if not request.text or request.speed < 0.5 or request.speed > 2.0:
        return {"error": "Invalid input"}
    
    # Generate TTS (Hebrew support in gTTS)
    tts = gTTS(request.text, lang='he', slow=request.speed < 1.0)  # Slow for <1.0
    with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as tmp:
        tts.save(tmp.name)
        audio_path = tmp.name
    
    # Stub timings: Estimate ~0.5s per word (improve with wave analysis later)
    words = request.text.split()
    timings = [{"word": w, "start": i * 0.5, "end": (i + 1) * 0.5} for i, w in enumerate(words)]
    
    return {"audioUrl": f"/audio?path={audio_path}", "timings": timings}  # Serve via endpoint

@app.get("/audio")
async def serve_audio(path: str = Query(...)):
    if not os.path.exists(path):
        return {"error": "Audio not found"}
    response = FileResponse(path, media_type="audio/wav")
    response.headers["Content-Disposition"] = "inline"  # Secure: No download prompt
    # Cleanup after serve (async task in production)
    return response

@app.get("/lexicon")
async def get_lexicon(word: str = Query(...)):
    # Secure: Sanitize word
    word = word.strip()
    if word not in lexicon:
        return {"error": "Word not found"}
    return lexicon[word]  # {ipa, morph}

# Morphology enhancement stub: Integrate hspell in generate_lexicon.py (run manually for now)
# Example: Add to generate_lexicon.py - import hspell; morph = hspell.analyze(word)