"""
preprocess.py
Basic text cleaning shared by training and inference, so the exact same
transformation is applied both times (avoids train/serve skew).
"""
import re

WHITESPACE_RE = re.compile(r"\s+")


def clean_text(text: str) -> str:
    if not isinstance(text, str):
        text = "" if text is None else str(text)
    text = text.strip()
    text = WHITESPACE_RE.sub(" ", text)
    return text


def combine_conversation(messages: list[str]) -> str:
    """Joins a list of message turns into one string, preserving turn
    boundaries as newlines (used by patterns.py to count turns)."""
    return "\n".join(clean_text(m) for m in messages if clean_text(m))
