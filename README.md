# ScamGuard — Initial Prototype

A machine learning system for detecting AI-assisted social-engineering scam communication in SMS/text conversations, including scam strategies not seen during training.
## Description

ScamGuard takes a pasted SMS conversation and:
1. Extracts a set of interpretable linguistic and social-engineering pattern signals (urgency language, authority claims, personalization, requests for action, links, phone numbers, money mentions).
2. Classifies the conversation as **scam** or **legitimate** using a baseline TF-IDF + Logistic Regression model.
3. Returns the classification, a confidence score, and the specific patterns that were detected.

This initial version also runs the proposal's central **generalization experiment**: one entire scam category (`virtual_kidnapping`) is withheld completely from training, then tested separately, to check whether the model still recognizes it as a scam despite never training on that category. Results are available at the `/metrics` endpoint.
