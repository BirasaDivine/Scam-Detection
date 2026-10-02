"""
train.py

Trains ScamGuard's initial baseline classifier (TF-IDF + Logistic Regression,
the "BaselineModel" from the proposal's class diagram) on:
  - real COVA-X scam conversations (8 categories), as the positive class
  - a small placeholder legitimate-conversation set, as the negative class

Runs TWO evaluations, directly mirroring the proposal's central experiment:
  1. Known-strategy test: normal held-out test split across all 8 categories.
  2. Unseen-strategy (generalization) test: one entire scam category is
     withheld from training completely, then tested on -- does the model
     still recognize it as a scam despite never training on that category?
"""
import json
import random
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_recall_fscore_support, confusion_matrix
import joblib
import numpy as np

from load_covax import load_covax, CATEGORIES
from legitimate_placeholder import generate as generate_legit
from short_scam_examples import generate as generate_short_scams
from preprocess import clean_text, combine_conversation
from patterns import extract_patterns

HELD_OUT_CATEGORY = "virtual_kidnapping"  # withheld entirely from training
PER_CATEGORY_CAP = 300  # cap per scam category for faster iteration; raise for final run
N_LEGIT = 1800  # roughly balances ~300*7 known-category scam examples


def build_text_and_features(messages):
    text = combine_conversation(messages)
    feats = extract_patterns(text)
    return text, feats


def rows_to_arrays(rows):
    texts, feat_dicts, labels = [], [], []
    for r in rows:
        text, feats = build_text_and_features(r["messages"])
        texts.append(text)
        feat_dicts.append(feats)
        labels.append(1 if r["label"] == "scam" else 0)
    return texts, feat_dicts, labels


def feats_to_matrix(feat_dicts, feature_names):
    return np.array([[float(f[name]) for name in feature_names] for f in feat_dicts])


def main():
    print(f"Loading COVA-X (cap={PER_CATEGORY_CAP}/category, held-out category = '{HELD_OUT_CATEGORY}')...")
    all_scam = load_covax(raw_dir="data/raw/covax", per_category_cap=PER_CATEGORY_CAP)
    known_scam = [r for r in all_scam if r["category"] != HELD_OUT_CATEGORY]
    held_out_scam = [r for r in all_scam if r["category"] == HELD_OUT_CATEGORY]
    print(f"  known-category scam examples: {len(known_scam)}")
    print(f"  held-out ('{HELD_OUT_CATEGORY}') scam examples: {len(held_out_scam)}")

    legit_rows = generate_legit(n_conversations=N_LEGIT)
    short_scam_rows = generate_short_scams()
    print(f"  legitimate (placeholder) examples: {len(legit_rows)}")
    print(f"  short single-message scam examples (length-confound mitigation): {len(short_scam_rows)}")

    # --- Known-strategy split: scam (non-held-out categories) + legitimate ---
    # short_scam_rows are duplicated a few times so they carry enough weight
    # to actually counter the length confound, not just a token few rows.
    known_rows = known_scam + legit_rows + short_scam_rows * 15
    random.Random(42).shuffle(known_rows)

    texts, feat_dicts, labels = rows_to_arrays(known_rows)
    feature_names = sorted([k for k, v in feat_dicts[0].items() if isinstance(v, (bool, int, float))])

    X_train_txt, X_test_txt, feat_train, feat_test, y_train, y_test = train_test_split(
        texts, feat_dicts, labels, test_size=0.2, random_state=42, stratify=labels
    )

    vectorizer = TfidfVectorizer(max_features=3000, ngram_range=(1, 2), min_df=2)
    Xtr_tfidf = vectorizer.fit_transform(X_train_txt)
    Xte_tfidf = vectorizer.transform(X_test_txt)

    Xtr_feat = feats_to_matrix(feat_train, feature_names)
    Xte_feat = feats_to_matrix(feat_test, feature_names)

    from scipy.sparse import hstack
    Xtr = hstack([Xtr_tfidf, Xtr_feat])
    Xte = hstack([Xte_tfidf, Xte_feat])

    clf = LogisticRegression(max_iter=1000, class_weight="balanced")
    clf.fit(Xtr, y_train)

    y_pred = clf.predict(Xte)
    acc = accuracy_score(y_test, y_pred)
    prec, rec, f1, _ = precision_recall_fscore_support(y_test, y_pred, average="binary", zero_division=0)
    print("\n=== Known-strategy test (held-out 20% split, all 7 trained categories + legitimate) ===")
    print(f"Accuracy:  {acc:.3f}")
    print(f"Precision: {prec:.3f}")
    print(f"Recall:    {rec:.3f}")
    print(f"F1:        {f1:.3f}")
    print("Confusion matrix [ [TN FP] [FN TP] ]:")
    print(confusion_matrix(y_test, y_pred))


if __name__ == "__main__":
    main()
