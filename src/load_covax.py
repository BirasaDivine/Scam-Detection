"""
load_covax.py
Loads real COVA-X conversation JSON files (Lochstampfor & Roy, 2026,
arXiv:2606.06879) from data/raw/Dataset/COVA-X_Dataset/<category>/*.json.

COVA-X is licensed research data (non-commercial, 12-month renewable access
per its TERMS file) -- it is NOT committed to this repo. See README for how
to request access and where to place the files locally.
"""
import json
import glob
import os
import random

CATEGORIES = [
    "bank", "romance", "grandparent", "government_impersonation",
    "medicare", "investment", "lottery", "virtual_kidnapping",
]


def _load_one(filepath: str) -> dict:
    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)
    messages = [turn.get("content", "") for turn in data.get("turns", [])]
    return {
        "conversation_id": data.get("conversation_id", ""),
        "messages": messages,
        "label": "scam",
        "category": data.get("scam_type", "unknown"),
    }


DEFAULT_RAW_DIR = "data/raw/Dataset/COVA-X_Dataset"


def load_covax(raw_dir: str = DEFAULT_RAW_DIR, per_category_cap: int | None = 300,
                seed: int = 42) -> list[dict]:
    """Loads COVA-X conversations, optionally capped per category for faster
    iteration during development. Set per_category_cap=None to load everything."""
    rng = random.Random(seed)
    rows = []
    for category in CATEGORIES:
        folder = os.path.join(raw_dir, category)
        files = sorted(glob.glob(os.path.join(folder, "*.json")))
        if not files:
            print(f"WARNING: no files found for category '{category}' in {folder}")
            continue
        if per_category_cap is not None and len(files) > per_category_cap:
            files = rng.sample(files, per_category_cap)
        for fp in files:
            try:
                rows.append(_load_one(fp))
            except Exception as exc:
                print(f"WARNING: skipped {fp} ({type(exc).__name__})")
    return rows


if __name__ == "__main__":
    rows = load_covax(per_category_cap=5)
    print(f"Loaded {len(rows)} sample conversations")
    print(rows[0])
