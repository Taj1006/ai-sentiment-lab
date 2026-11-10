"""Small sentiment boundary; the default analyzer uses TextBlob's built-in rules."""

import math


def classify_polarity(score: float) -> str:
    """Map a finite TextBlob polarity in [-1, 1] to a display label."""
    if not math.isfinite(score) or not -1.0 <= score <= 1.0:
        raise ValueError("Polarity must be finite and between -1 and 1.")
    if score > 0:
        return "Positive"
    if score < 0:
        return "Negative"
    return "Neutral"


def analyze_text(text: str, analyzer=None) -> tuple[float, str]:
    """Return (polarity, label); allow a fake analyzer for dependency-free tests."""
    if not text.strip():
        raise ValueError("Enter non-empty text to analyze.")
    if analyzer is None:
        # Lazy import keeps validation/classification independently testable.
        from textblob import TextBlob

        analyzer = TextBlob
    score = float(analyzer(text).sentiment.polarity)
    return score, classify_polarity(score)
