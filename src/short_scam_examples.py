"""
short_scam_examples.py

COVA-X conversations are long, multi-turn phone-call-style transcripts.
Without any short positive (scam) examples, a classifier can learn "long =
scam, short = legitimate" as a shortcut instead of learning actual content
signals -- exactly the kind of spurious confound an initial-version demo
should not quietly ship with.

These are a small number of hand-written, classic single-message SMS
phishing texts (the kind actually cited at scale in the proposal's own
literature, e.g. Agarwal et al., 2025) used ONLY to balance conversation
length in the positive class. Not a substitute for a real short-SMS dataset.
"""

SHORT_SCAMS = [
    "Dear customer, your account has been suspended. Click here to verify immediately: http://bit.ly/verify-now",
    "URGENT: Your package delivery failed. Pay a $2 redelivery fee at http://trackpkg.co",
    "Your bank card has been locked due to suspicious activity. Call 1-800-555-0199 now to unlock it.",
    "Congratulations! You've won a $1000 gift card. Claim now at http://prize-claim.co before it expires.",
    "IRS Notice: You owe back taxes. Failure to respond within 24 hours will result in legal action.",
    "We noticed unusual login activity. Verify your identity now: http://secure-check.co",
    "Your subscription payment failed. Update your billing info immediately to avoid service loss: http://billing-fix.co",
    "Final notice: your account will be permanently closed today unless you confirm your details now.",
    "Hi, this is your delivery courier. We need you to pay a customs fee of $3.50 to release your parcel.",
    "Security Alert: someone tried to access your account from a new device. Click to secure it now.",
    "You have an unclaimed refund of $450 waiting. Submit your bank details to receive it today.",
    "Your Netflix payment was declined. Update your card now or lose access: http://netflix-billing.co",
]


def generate(seed: int = 3) -> list[dict]:
    return [
        {
            "conversation_id": f"short_scam_{i:03d}",
            "messages": [text],
            "label": "scam",
            "category": "short_sms_phishing",
        }
        for i, text in enumerate(SHORT_SCAMS)
    ]
