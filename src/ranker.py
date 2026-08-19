"""
ranker.py — Resume Ranking & Scoring Module
============================================
Core ranking engine: computes TF-IDF cosine similarity between a job
description and each resume, then blends in a skill-overlap score to produce
a final explainable composite rank score.

Ranking Formula:
  final_score = (tfidf_weight × cosine_similarity) + (skill_weight × skill_overlap_ratio)

Where tfidf_weight + skill_weight = 1.0  (defaults: 0.70 + 0.30)
"""

from __future__ import annotations
import logging
from dataclasses import dataclass, field

import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

logger = logging.getLogger(__name__)


# ══════════════════════════════════════════════════════════════════════════════
# DATA STRUCTURES
# ══════════════════════════════════════════════════════════════════════════════

@dataclass
class CandidateResult:
    """Holds all scoring information for a single candidate."""
    name:               str               # Candidate name or filename
    raw_text:           str               # Original extracted resume text
    processed_text:     str               # Lemmatised text used for TF-IDF
    tfidf_score:        float = 0.0       # Cosine similarity score (0–1)
    skill_score:        float = 0.0       # Skill overlap ratio (0–1)
    final_score:        float = 0.0       # Weighted composite score (0–1)
    final_score_pct:    float = 0.0       # final_score × 100 (for display)
    matched_skills:     list  = field(default_factory=list)
    missing_skills:     list  = field(default_factory=list)
    extra_skills:       list  = field(default_factory=list)
    top_tfidf_terms:    list  = field(default_factory=list)  # Top-10 TF-IDF terms


# ══════════════════════════════════════════════════════════════════════════════
# TFIDF + COSINE SIMILARITY
# ══════════════════════════════════════════════════════════════════════════════

def compute_tfidf_scores(
    jd_processed: str,
    resumes_processed: list[str],
) -> tuple[list[float], TfidfVectorizer, np.ndarray]:
    """
    Vectorize the job description and all resumes with TF-IDF, then
    compute cosine similarity between the JD and each resume.

    Args:
        jd_processed:       Lemmatised JD text.
        resumes_processed:  List of lemmatised resume texts.

    Returns:
        Tuple of:
        - scores (list[float]): Cosine similarity per resume.
        - vectorizer (TfidfVectorizer): Fitted vectorizer (for term extraction).
        - tfidf_matrix (np.ndarray): Full TF-IDF matrix (JD + all resumes).
    """
    # Combine JD and resumes so TF-IDF vocabulary covers all documents
    all_docs = [jd_processed] + resumes_processed

    # TF-IDF configuration:
    #   ngram_range=(1,2) captures bigrams like "machine learning"
    #   max_features=10000 caps vocabulary for performance
    #   min_df=1 keeps rare but potentially critical terms
    vectorizer = TfidfVectorizer(
        ngram_range=(1, 2),
        max_features=10_000,
        sublinear_tf=True,   # Apply log(1+tf) for smoother term weighting
        min_df=1,
    )
    tfidf_matrix = vectorizer.fit_transform(all_docs)

    # JD vector is the first row; resume vectors are rows 1..N
    jd_vector      = tfidf_matrix[0:1]
    resume_vectors = tfidf_matrix[1:]

    # Cosine similarity: measures angle between JD and each resume vector
    similarities = cosine_similarity(jd_vector, resume_vectors)[0]
    scores = [float(s) for s in similarities]

    return scores, vectorizer, tfidf_matrix


def get_top_tfidf_terms(
    vectorizer: TfidfVectorizer,
    doc_vector,
    top_n: int = 10,
) -> list[str]:
    """
    Return the top-N most important terms for a given document TF-IDF vector.

    Args:
        vectorizer:  Fitted TfidfVectorizer.
        doc_vector:  Sparse TF-IDF vector for a single document.
        top_n:       Number of top terms to return.

    Returns:
        List of top-N term strings.
    """
    feature_names = vectorizer.get_feature_names_out()
    dense = doc_vector.toarray().flatten()
    # Argsort descending → pick top N indices
    top_indices = dense.argsort()[::-1][:top_n]
    return [feature_names[i] for i in top_indices if dense[i] > 0]


# ══════════════════════════════════════════════════════════════════════════════
# COMPOSITE SCORE CALCULATOR
# ══════════════════════════════════════════════════════════════════════════════

def compute_composite_scores(
    jd_processed:        str,
    resumes_processed:   list[str],
    skill_results:       list[dict],
    candidate_names:     list[str],
    candidate_raw_texts: list[str],
    tfidf_weight:        float = 0.70,
    skill_weight:        float = 0.30,
) -> list[CandidateResult]:
    """
    Orchestrate full scoring for all candidates:
    1. Run TF-IDF + cosine similarity.
    2. Blend with skill overlap ratio.
    3. Attach top TF-IDF terms and skill breakdown.

    Args:
        jd_processed:        Preprocessed JD text.
        resumes_processed:   List of preprocessed resume texts.
        skill_results:       List of skill-match dicts from skills.compute_skill_match().
        candidate_names:     List of candidate names/filenames.
        candidate_raw_texts: List of original raw resume texts.
        tfidf_weight:        Weight for TF-IDF score component (default 0.70).
        skill_weight:        Weight for skill overlap component (default 0.30).

    Returns:
        List of CandidateResult objects, sorted descending by final_score.
    """
    if not resumes_processed:
        return []

    # ── Step 1: TF-IDF cosine similarity ─────────────────────────────────────
    tfidf_scores, vectorizer, tfidf_matrix = compute_tfidf_scores(
        jd_processed, resumes_processed
    )

    results = []
    for i, name in enumerate(candidate_names):
        tfidf_score  = tfidf_scores[i]
        skill_info   = skill_results[i] if i < len(skill_results) else {}
        skill_score  = skill_info.get("skill_overlap_ratio", 0.0)

        # ── Step 2: Weighted composite score ─────────────────────────────────
        final_score = (tfidf_weight * tfidf_score) + (skill_weight * skill_score)

        # ── Step 3: Extract top TF-IDF terms for this resume ─────────────────
        # Offset by 1 because row 0 is the JD in the matrix
        resume_vector = tfidf_matrix[i + 1]
        top_terms = get_top_tfidf_terms(vectorizer, resume_vector, top_n=10)

        result = CandidateResult(
            name=name,
            raw_text=candidate_raw_texts[i] if i < len(candidate_raw_texts) else "",
            processed_text=resumes_processed[i],
            tfidf_score=round(tfidf_score, 4),
            skill_score=round(skill_score, 4),
            final_score=round(final_score, 4),
            final_score_pct=round(final_score * 100, 2),
            matched_skills=skill_info.get("matched_skills", []),
            missing_skills=skill_info.get("missing_skills", []),
            extra_skills=skill_info.get("extra_skills", []),
            top_tfidf_terms=top_terms,
        )
        results.append(result)

    # ── Step 4: Sort by final score descending (best match first) ─────────────
    results.sort(key=lambda r: r.final_score, reverse=True)

    return results


# ══════════════════════════════════════════════════════════════════════════════
# RESULTS → DATAFRAME
# ══════════════════════════════════════════════════════════════════════════════

def results_to_dataframe(results: list[CandidateResult]) -> pd.DataFrame:
    """
    Convert a ranked list of CandidateResult objects into a display DataFrame.

    Returns columns:
    Rank | Candidate | Match Score (%) | TF-IDF Score | Skill Score | Matched Skills | Missing Skills
    """
    rows = []
    for rank, r in enumerate(results, start=1):
        rows.append({
            "Rank":              rank,
            "Candidate":         r.name,
            "Match Score (%)":   r.final_score_pct,
            "TF-IDF Score":      round(r.tfidf_score * 100, 2),
            "Skill Score (%)":   round(r.skill_score * 100, 2),
            "Matched Skills":    ", ".join(r.matched_skills) if r.matched_skills else "—",
            "Missing Skills":    ", ".join(r.missing_skills) if r.missing_skills else "—",
            "Top Keywords":      ", ".join(r.top_tfidf_terms[:5]),
        })

    return pd.DataFrame(rows)
