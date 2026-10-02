"""
legitimate_placeholder.py

COVA-X (the real dataset this project uses) contains ONLY scam conversations
across 8 categories -- it has no "legitimate" class to contrast against.
This small, clearly-synthetic set of everyday conversations stands in as the
negative class for this initial prototype, so ScamGuard can demonstrate
scam-vs-legitimate classification end to end.

This is a placeholder, not a dataset: it exists to unblock the demo. The
proposal's planned replacement is a real non-scam SMS source (e.g. the
legitimate portion of a public smishing dataset).
"""
import random

random.seed(7)

LEGIT_CONVERSATIONS = [
    ["Hey, are we still on for lunch tomorrow?", "Yes! 1pm works for me.", "Great, see you then."],
    ["Your order #4521 has shipped.", "Thanks for the update!"],
    ["Mom, can you pick me up after practice?", "Sure, I'll be there at 5."],
    ["Reminder: dentist appointment on Friday at 10am.", "Got it, thank you."],
    ["Hi, just checking in, how was your trip?", "It was great, I'll tell you about it later."],
    ["Can you send me the notes from today's lecture?", "Sure, I'll email them tonight."],
    ["Happy birthday! Hope you have a great day.", "Thank you so much!"],
    ["Are you coming to the game on Saturday?", "Yes, I'll meet you there at noon."],
    ["Don't forget to bring the charger when you come over.", "Will do, see you soon."],
    ["The meeting got moved to 3pm, is that still okay?", "Yes that works for me, thanks for the heads up."],
    ["Can you grab milk on your way home?", "Sure thing, anything else?"],
    ["Your package was delivered to the front desk.", "Perfect, I'll pick it up this evening."],
    ["Let's catch up this weekend, free Saturday?", "Saturday works, let's do coffee at 10."],
    ["I finished the report, sending it over now.", "Thanks, I'll review it in the morning."],
    ["Traffic is bad, I'll be about 15 minutes late.", "No worries, drive safe."],
    # A few longer, multi-turn examples so "legitimate" isn't confounded with
    # "short" the way it would be if every negative example were one or two lines.
    [
        "Hey, did you see the email from the landlord about the inspection?",
        "Yeah, it's scheduled for next Tuesday at 2pm, is that okay for you?",
        "That should work, I'll try to be home by then.",
        "Great, I'll let him know. Do we need to clean anything specific before he comes?",
        "Maybe just tidy the kitchen and the hallway, should be fine otherwise.",
        "Sounds good, I'll handle the kitchen tonight.",
    ],
    [
        "Hi, just wanted to check if you're still free for the study group tomorrow.",
        "Yes, still on. Library at 4pm like last time?",
        "Works for me. Should we bring the practice questions from chapter 6?",
        "Good idea, I'll print a few extra copies for everyone.",
        "Perfect, see you there.",
    ],
    [
        "Mom, I landed safely, just waiting for my luggage now.",
        "Glad to hear it! Let me know when you're on your way home.",
        "Will do, should be about an hour with traffic.",
        "Okay, dinner will be ready when you get here.",
        "Thank you, can't wait, I'm starving.",
    ],
]


def generate(n_conversations: int = 1200, seed: int = 7) -> list[dict]:
    rng = random.Random(seed)
    rows = []
    for i in range(n_conversations):
        base = rng.choice(LEGIT_CONVERSATIONS)
        rows.append({
            "conversation_id": f"legit_{i:05d}",
            "messages": list(base),
            "label": "legitimate",
            "category": "legitimate",
        })
    return rows
