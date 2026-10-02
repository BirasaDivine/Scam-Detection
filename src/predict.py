"""
predict.py
Loads the trained baseline model once and exposes a single predict_conversation()
function used by the FastAPI app. Keeping this separate from app/main.py means
the same prediction logic could later be reused by a CLI or batch script.
"""
import json
import os
import joblib
import numpy as np
from scipy.sparse import hstack

from preprocess import combine_conversation
from patterns import extract_patterns, pattern_summary

MODELS_DIR = os.path.join(os.path.dirname(__file__), "..", "models")

_clf = None
_vectorizer = None
_feature_names = None


def _load_artifacts():
    global _clf, _vectorizer, _feature_names
    if _clf is None:
        _clf = joblib.load(os.path.join(MODELS_DIR, "baseline_model.joblib"))
        _vectorizer = joblib.load(os.path.join(MODELS_DIR, "vectorizer.joblib"))
        with open(os.path.join(MODELS_DIR, "feature_names.json")) as f:
            _feature_names = json.load(f)


def predict_conversation(raw_text: str) -> dict:
    """
    raw_text: the full conversation as pasted by the user (one message per
    line, or a single message).
    Returns a dict with label, probability, and the detected pattern list.
    """
    _load_artifacts()

    messages = [line for line in raw_text.split("\n") if line.strip()]
    if not messages:
        messages = [raw_text]

    text = combine_conversation(messages)
    features = extract_patterns(text)

    X_tfidf = _vectorizer.transform([text])
    X_feat = np.array([[float(features[name]) for name in _feature_names]])
    X = hstack([X_tfidf, X_feat])

    proba = _clf.predict_proba(X)[0]
    pred_class = int(_clf.predict(X)[0])
    label = "scam" if pred_class == 1 else "legitimate"
    confidence = float(proba[pred_class])

    return {
        "label": label,
        "confidence": round(confidence, 3),
        "detected_patterns": pattern_summary(features),
        "raw_features": features,
    }


if __name__ == "__main__":
    sample = "Dear customer, your account has been suspended. Click here to verify immediately: http://bit.ly/verify"
    print(predict_conversation(sample))
