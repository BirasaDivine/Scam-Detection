"""
app/main.py
ScamGuard initial-version backend API.

Run with:
    uvicorn app.main:app --reload --port 8000
(from the project root, so the relative model paths resolve correctly)
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel

from predict import predict_conversation

app = FastAPI(title="ScamGuard API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

STATIC_DIR = os.path.join(os.path.dirname(__file__), "..", "static")


class ConversationRequest(BaseModel):
    conversation: str


class AnalyzeResponse(BaseModel):
    label: str
    confidence: float
    detected_patterns: list[str]


@app.get("/")
def serve_index():
    return FileResponse(os.path.join(STATIC_DIR, "index.html"))


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/analyze", response_model=AnalyzeResponse)
def analyze(req: ConversationRequest):
    result = predict_conversation(req.conversation)
    return {
        "label": result["label"],
        "confidence": result["confidence"],
        "detected_patterns": result["detected_patterns"],
    }


app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
