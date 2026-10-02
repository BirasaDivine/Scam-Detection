"""
patterns.py
Lightweight, rule-based pattern extraction for ScamGuard's initial prototype.

This is a simplified stand-in for the full PatternExtractor described in the
proposal (which uses learned linguistic/conversational/social-engineering
feature maps). For this initial version, each pattern is a simple, explicit,
inspectable function -- easy to demo, easy to explain to a supervisor, and
easy to extend later with the real feature-learning pipeline.
"""
import re
import math

URGENCY_WORDS = [
    "urgent", "immediately", "now", "asap", "act now", "expire", "expires",
    "expiring", "limited time", "last chance", "warning", "suspended",
    "locked", "verify now", "final notice",
]

AUTHORITY_WORDS = [
    "bank", "irs", "tax", "government", "police", "court", "official",
    "support team", "customer service", "security department", "agent",
]

PERSONALIZATION_MARKERS = [
    "dear customer", "dear user", "valued customer", "hello", "hi ",
]

ACTION_REQUEST_WORDS = [
    "click", "click here", "login", "log in", "verify", "confirm",
    "update your", "send money", "transfer", "provide your", "call now",
    "reply with",
]

URL_PATTERN = re.compile(r"(https?://\S+|www\.\S+|bit\.ly/\S+)", re.IGNORECASE)
PHONE_PATTERN = re.compile(r"\b(\+?\d[\d\-\s]{7,}\d)\b")
MONEY_PATTERN = re.compile(r"(\$\s?\d+|\d+\s?(usd|rwf|frw)\b)", re.IGNORECASE)


def _contains_any(text: str, words: list[str]) -> bool:
    text_lower = text.lower()
    return any(w in text_lower for w in words)


def extract_patterns(text: str) -> dict:
    """
    Extracts a small set of interpretable linguistic / conversational /
    social-engineering pattern signals from a single message or an entire
    conversation (messages joined with newlines).

    Returns a dict of {pattern_name: bool/int} -- both used as model features
    and shown to the user as "detected patterns" in the UI.
    """
    text = text or ""
    lines = [l for l in text.split("\n") if l.strip()]

    features = {
        "has_urgency_language": _contains_any(text, URGENCY_WORDS),
        "has_authority_claim": _contains_any(text, AUTHORITY_WORDS),
        "has_personalization": _contains_any(text, PERSONALIZATION_MARKERS),
        "requests_action": _contains_any(text, ACTION_REQUEST_WORDS),
        "contains_url": bool(URL_PATTERN.search(text)),
        "contains_phone_number": bool(PHONE_PATTERN.search(text)),
        "mentions_money": bool(MONEY_PATTERN.search(text)),
        # Log-scaled so these don't dwarf the boolean flags and tiny TF-IDF
        # values once combined into one feature matrix (raw lengths like 146
        # or 494 were swamping everything else and making the model mostly
        # learn "long conversation = scam" instead of the actual patterns).
        "message_length_scaled": math.log1p(len(text)) / 10.0,
        "turn_count_scaled": math.log1p(len(lines) if len(lines) > 1 else 1) / 5.0,
        "exclamation_count": min(text.count("!"), 5) / 5.0,
    }
    return features


def pattern_summary(features: dict) -> list[str]:
    """Human-readable list of which patterns fired, for display in the UI."""
    labels = {
        "has_urgency_language": "Urgency language detected",
        "has_authority_claim": "Claims authority (bank/government/support)",
        "has_personalization": "Generic personalization greeting",
        "requests_action": "Requests an action (click/verify/send money)",
        "contains_url": "Contains a link",
        "contains_phone_number": "Contains a phone number",
        "mentions_money": "Mentions a monetary amount",
    }
    fired = [label for key, label in labels.items() if features.get(key)]
    return fired
