"""
skills.py — Skill Extraction & Matching Module
================================================
Defines a comprehensive predefined skills taxonomy and uses spaCy's
PhraseMatcher to identify which skills appear in job descriptions and resumes.
Also computes matched skills, missing skills, and skill overlap ratio.
"""

from __future__ import annotations
import logging
from spacy.matcher import PhraseMatcher

logger = logging.getLogger(__name__)

# ══════════════════════════════════════════════════════════════════════════════
# SKILL TAXONOMY
# A curated list of ~250+ skills grouped by domain.
# This predefined taxonomy avoids needing a trained NER model.
# ══════════════════════════════════════════════════════════════════════════════

SKILLS_TAXONOMY = {
    # ── Programming Languages ─────────────────────────────────────────────────
    "Programming Languages": [
        "python", "java", "javascript", "typescript", "c++", "c#", "c",
        "r", "go", "golang", "rust", "swift", "kotlin", "scala", "ruby",
        "php", "perl", "matlab", "bash", "shell scripting", "powershell",
        "vba", "dart", "julia",
    ],

    # ── Web Development ───────────────────────────────────────────────────────
    "Web Development": [
        "html", "css", "react", "react.js", "angular", "vue", "vue.js",
        "node.js", "express", "django", "flask", "fastapi", "spring boot",
        "rest api", "graphql", "bootstrap", "tailwind", "next.js", "nuxt",
        "webpack", "sass", "jquery", "redux", "gatsby", "svelte",
    ],

    # ── Data Science & Machine Learning ───────────────────────────────────────
    "Data Science & ML": [
        "machine learning", "deep learning", "neural networks", "nlp",
        "natural language processing", "computer vision", "data science",
        "data analysis", "statistical analysis", "predictive modeling",
        "feature engineering", "model training", "model deployment",
        "scikit-learn", "tensorflow", "pytorch", "keras", "xgboost",
        "lightgbm", "pandas", "numpy", "scipy", "matplotlib", "seaborn",
        "plotly", "spacy", "nltk", "hugging face", "transformers",
        "regression", "classification", "clustering", "random forest",
        "decision tree", "support vector machine", "svm", "k-means",
        "a/b testing", "time series", "forecasting",
    ],

    # ── Databases ─────────────────────────────────────────────────────────────
    "Databases": [
        "sql", "mysql", "postgresql", "sqlite", "oracle", "mongodb",
        "redis", "cassandra", "dynamodb", "elasticsearch", "firebase",
        "nosql", "database design", "query optimization", "stored procedures",
        "data warehousing", "etl", "data pipeline",
    ],

    # ── Cloud & DevOps ────────────────────────────────────────────────────────
    "Cloud & DevOps": [
        "aws", "azure", "google cloud", "gcp", "docker", "kubernetes",
        "terraform", "ansible", "jenkins", "ci/cd", "git", "github",
        "gitlab", "bitbucket", "linux", "unix", "nginx", "apache",
        "microservices", "serverless", "devops", "sre", "monitoring",
        "prometheus", "grafana", "datadog",
    ],

    # ── Data Engineering ──────────────────────────────────────────────────────
    "Data Engineering": [
        "apache spark", "hadoop", "kafka", "airflow", "dbt", "snowflake",
        "redshift", "bigquery", "databricks", "data lake", "data mesh",
        "tableau", "power bi", "looker", "qlik", "excel", "google sheets",
    ],

    # ── Human Resources ───────────────────────────────────────────────────────
    "Human Resources": [
        "recruitment", "talent acquisition", "onboarding", "performance management",
        "employee relations", "compensation", "benefits", "payroll",
        "hris", "workday", "successfactors", "bamboohr", "ats",
        "applicant tracking", "job posting", "candidate screening",
        "behavioral interviewing", "training and development", "l&d",
        "learning and development", "succession planning", "workforce planning",
        "hr analytics", "people analytics", "organizational development",
        "change management", "diversity and inclusion", "dei",
        "employment law", "labor relations", "conflict resolution",
    ],

    # ── Project & Product Management ──────────────────────────────────────────
    "Project & Product Management": [
        "agile", "scrum", "kanban", "jira", "confluence", "project management",
        "product management", "product roadmap", "stakeholder management",
        "risk management", "pmp", "prince2", "waterfall", "lean",
        "six sigma", "okr", "kpi", "budget management", "resource planning",
        "sprint planning", "backlog grooming", "user stories",
    ],

    # ── Marketing & Sales ─────────────────────────────────────────────────────
    "Marketing & Sales": [
        "digital marketing", "seo", "sem", "google ads", "social media marketing",
        "content marketing", "email marketing", "crm", "salesforce", "hubspot",
        "market research", "brand management", "copywriting", "analytics",
        "google analytics", "lead generation", "sales strategy",
        "business development", "customer acquisition",
    ],

    # ── Finance & Accounting ──────────────────────────────────────────────────
    "Finance & Accounting": [
        "financial analysis", "financial modeling", "accounting", "bookkeeping",
        "quickbooks", "sap", "erp", "budgeting", "forecasting", "auditing",
        "tax preparation", "gaap", "ifrs", "accounts payable", "accounts receivable",
        "balance sheet", "income statement", "cash flow", "valuation",
        "investment analysis", "cpa", "cfa",
    ],

    # ── Soft Skills ───────────────────────────────────────────────────────────
    "Soft Skills": [
        "communication", "leadership", "teamwork", "problem solving",
        "critical thinking", "time management", "adaptability", "creativity",
        "collaboration", "attention to detail", "customer service",
        "presentation skills", "negotiation", "mentoring", "coaching",
        "strategic thinking", "decision making", "analytical skills",
        "multitasking", "organizational skills",
    ],

    # ── Testing & QA ──────────────────────────────────────────────────────────
    "Testing & QA": [
        "unit testing", "integration testing", "selenium", "pytest",
        "jest", "cypress", "test automation", "qa", "quality assurance",
        "postman", "api testing", "load testing", "performance testing",
    ],

    # ── Security ─────────────────────────────────────────────────────────────
    "Cybersecurity": [
        "cybersecurity", "network security", "penetration testing",
        "ethical hacking", "firewall", "encryption", "ssl", "tls",
        "siem", "vulnerability assessment", "iso 27001", "soc",
    ],
}

# Flatten all skills into a single deduplicated list for easy access
ALL_SKILLS: list[str] = list({
    skill
    for skills in SKILLS_TAXONOMY.values()
    for skill in skills
})


# ══════════════════════════════════════════════════════════════════════════════
# PHRASE MATCHER
# ══════════════════════════════════════════════════════════════════════════════

_MATCHER = None  # Module-level cache for the PhraseMatcher


def get_matcher(nlp):
    """
    Build and cache a spaCy PhraseMatcher loaded with all taxonomy skills.
    Uses LOWER attribute matching so "Python" == "python" == "PYTHON".
    """
    global _MATCHER
    if _MATCHER is None:
        _MATCHER = PhraseMatcher(nlp.vocab, attr="LOWER")
        # Create pattern docs for each skill phrase
        patterns = [nlp.make_doc(skill) for skill in ALL_SKILLS]
        _MATCHER.add("SKILLS", patterns)
        logger.info(f"PhraseMatcher built with {len(ALL_SKILLS)} skill patterns.")
    return _MATCHER


def extract_skills(doc, nlp) -> set[str]:
    """
    Extract skills present in a spaCy Doc using PhraseMatcher.

    Args:
        doc:  A spaCy Doc object (output of nlp(text)).
        nlp:  The loaded spaCy Language model.

    Returns:
        Set of matched skill strings (lowercased, normalised).
    """
    matcher = get_matcher(nlp)
    matches = matcher(doc)

    found_skills = set()
    for _, start, end in matches:
        skill_text = doc[start:end].text.lower()
        found_skills.add(skill_text)

    return found_skills


def compute_skill_match(
    jd_skills: set[str],
    resume_skills: set[str],
) -> dict:
    """
    Compare resume skills against required job-description skills.

    Args:
        jd_skills:     Skills extracted from the job description.
        resume_skills: Skills extracted from a candidate's resume.

    Returns:
        Dictionary with:
        - matched_skills (list):  Skills in both JD and resume.
        - missing_skills (list):  Skills required by JD but absent from resume.
        - extra_skills   (list):  Skills in resume not explicitly required.
        - skill_overlap_ratio (float): matched / max(total required, 1) in [0, 1].
    """
    matched = sorted(jd_skills & resume_skills)
    missing = sorted(jd_skills - resume_skills)
    extra   = sorted(resume_skills - jd_skills)

    # Overlap ratio: how many required skills does this candidate cover?
    overlap_ratio = len(matched) / max(len(jd_skills), 1)

    return {
        "matched_skills":     matched,
        "missing_skills":     missing,
        "extra_skills":       extra,
        "skill_overlap_ratio": round(overlap_ratio, 4),
    }
