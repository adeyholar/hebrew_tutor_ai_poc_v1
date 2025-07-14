from fastapi import FastAPI, APIRouter, HTTPException, UploadFile, File
from pydantic import BaseModel
from dotenv import load_dotenv
import os
import torch
import whisperx
import subprocess
import tempfile
import json
import sqlalchemy as sa

load_dotenv()
app = FastAPI()

device = os.getenv("DEVICE", "cuda" if torch.cuda.is_available() else "cpu")

# DB setup...

# Health...

# Agent 1...
pronunciation_router = APIRouter(prefix="/pronunciation")
class PronunciationResponse(BaseModel):
    score: float
    feedback: str
    ipa: str

@pronunciation_router.post("/")
async def assess_pronunciation(audio: UploadFile = File(...)):
    if not audio.filename.endswith(('.mp3', '.wav')):
        raise HTTPException(400, "Invalid audio")
    model = whisperx.load_model("large-v2", device=device, compute_type="float16")
    result = model.transcribe(audio.file, language="he")
    score = 0.95  # Stub; full: confidence-based
    return PronunciationResponse(score=score, feedback="Good pronunciation", ipa="/example ipa/")

# Agent 2...
reading_router = APIRouter(prefix="/reading")
class ReadingRequest(BaseModel):
    text: str

class ReadingResponse(BaseModel):
    audio_url: str
    timings: list[dict]

@reading_router.post("/")
async def read_companion(request: ReadingRequest):
    with tempfile.TemporaryDirectory() as temp_dir:
        text_path = os.path.join(temp_dir, "input.txt")
        audio_path = os.path.join(temp_dir, "input.mp3")
        with open(text_path, 'w', encoding='utf-8') as f:
            f.write(request.text)
        subprocess.run(["copy", "data/tanakh.mp3", audio_path], shell=True, check=True)
        subprocess.run(["mfa", "align", "--clean", "--output_format", "json", temp_dir, "hebrew_mfa", "hebrew_mfa", temp_dir], check=True)
        output_path = os.path.join(temp_dir, "input.json")  # MFA output
        with open(output_path, 'r') as f:
            data = json.load(f)
        timings = [{"word": w['text'], "start": w['begin'], "end": w['end']} for w in data['tiers'][0]['items']]  # Parse MFA JSON
    return ReadingResponse(audio_url="data/tanakh.mp3", timings=timings)

app.include_router(pronunciation_router)
app.include_router(reading_router)