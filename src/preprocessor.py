"""
preprocessor.py — NLP Preprocessing Module
============================================
Cleans and preprocesses raw resume/job-description text using spaCy.
Pipeline: clean raw text → tokenize → remove stopwords → lemmatize.
Returns both a clean string (for TF-IDF) and a spaCy Doc (for matching).
"""

import re
import logging

import spacy
from spacy.language import Language

logger = logging.getLogger(__name__)

# ── Load spaCy model once at module level (cached for performance) ─────────────
_NLP_MODEL: Language | None = None


def get_nlp() -> Language:
    """
    Load and cache the spaCy language model.
    Tries en_core_web_md first (has word vectors), falls back to en_core_web_sm.
    """
    global _NLP_MODEL
    if _NLP_MODEL is None:
        for model_name in ("en_core_web_md", "en_core_web_sm"):
            try:
                _NLP_MODEL = spacy.load(model_name)
                logger.info(f"Loaded spaCy model: {model_name}")
                break
            except OSError:
                logger.warning(f"spaCy model '{model_name}' not found, trying next...")
        if _NLP_MODEL is None:
            raise RuntimeError(
                "No spaCy model found. Run: python -m spacy download en_core_web_sm"
            )
    return _NLP_MODEL


# ── Regular expressions for noise removal ─────────────────────────────────────
_RE_EMAIL    = re.compile(r"\S+@\S+\.\S+")           # Strip email addresses
_RE_URL      = re.compile(r"https?://\S+|www\.\S+")  # Strip URLs
_RE_PHONE    = re.compile(r"\+?[\d\s\-().]{7,}")      # Strip phone numbers
_RE_SPECIAL  = re.compile(r"[^a-zA-Z0-9\s]")         # Remove special characters
_RE_SPACES   = re.compile(r"\s+")                     # Collapse whitespace


def clean_text(text: str) -> str:
    """
    Remove noise from raw resume text:
    emails, URLs, phone numbers, special characters, and extra whitespace.

    Args:
        text: Raw input string.

    Returns:
        Lowercased, whitespace-normalised string.
    """
    text = _RE_EMAIL.sub(" ", text)
    text = _RE_URL.sub(" ", text)
    text = _RE_PHONE.sub(" ", text)
    text = _RE_SPECIAL.sub(" ", text)
    text = _RE_SPACES.sub(" ", text)
    return text.strip().lower()


def preprocess(text: str) -> tuple[str, object]:
    """
    Full NLP preprocessing pipeline for a single text document.

    Steps:
    1. Clean raw text (remove noise)
    2. Parse with spaCy (tokenisation + POS tagging + lemmatisation)
    3. Filter: remove stopwords, punctuation, and very short tokens (< 2 chars)
    4. Lemmatise each remaining token

    Args:
        text: Raw input string.

    Returns:
        Tuple of:
        - processed_str (str): Space-joined lemmas — fed into TF-IDF
        - doc (spacy.tokens.Doc): Full spaCy Doc — used for PhraseMatcher skill extraction
    """
    nlp = get_nlp()

    # Step 1: clean raw noise
    cleaned = clean_text(text)

    # Step 2: parse with spaCy (limit to 1M chars to avoid memory issues)
    doc = nlp(cleaned[:1_000_000])

    # Step 3 & 4: filter tokens and lemmatise
    lemmas = [
        token.lemma_        # Base form (e.g., "running" → "run")
        for token in doc
        if not token.is_stop       # Skip common stopwords
        and not token.is_punct     # Skip punctuation
        and not token.is_space     # Skip whitespace tokens
        and len(token.text) > 1   # Skip single-character tokens
    ]

    processed_str = " ".join(lemmas)
    return processed_str, doc


def preprocess_batch(texts: list[str]) -> list[tuple[str, object]]:
    """
    Batch preprocessing for multiple texts using spaCy's efficient nlp.pipe().

    Args:
        texts: List of raw text strings.

    Returns:
        List of (processed_str, doc) tuples in the same order.
    """
    nlp = get_nlp()
    results = []

    # Clean all texts first
    cleaned_texts = [clean_text(t)[:1_000_000] for t in texts]

    # Use nlp.pipe for batched, multi-threaded processing
    docs = list(nlp.pipe(cleaned_texts, batch_size=20))

    for doc in docs:
        lemmas = [
            token.lemma_
            for token in doc
            if not token.is_stop
            and not token.is_punct
            and not token.is_space
            and len(token.text) > 1
        ]
        results.append((" ".join(lemmas), doc))

    return results
