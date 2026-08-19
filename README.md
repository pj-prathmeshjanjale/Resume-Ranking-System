# RecruitIQ — AI-Based Resume Ranking System

<div align="center">

![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=flat-square&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.32%2B-FF4B4B?style=flat-square&logo=streamlit&logoColor=white)
![spaCy](https://img.shields.io/badge/spaCy-3.8-09A3D5?style=flat-square&logo=spacy&logoColor=white)
![scikit-learn](https://img.shields.io/badge/scikit--learn-1.4%2B-F7931E?style=flat-square&logo=scikit-learn&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-22c55e?style=flat-square)

**An AI-powered, fully offline resume screening tool that ranks candidates against a job description using NLP, TF-IDF similarity, and a 250+ skill taxonomy.**

[Live Demo](#-deploy-to-streamlit-cloud) · [Quick Start](#-quick-start) · [How It Works](#-how-the-ranking-algorithm-works) · [Project Metadata](#-project-metadata)

</div>

---

## 📋 Project Metadata

| Field | Value |
|---|---|
| **Project ID** | P17 |
| **Domain** | Human Resources |
| **AI Technologies** | NLP, Ranking Algorithms |
| **Tools** | Python, spaCy, Streamlit |
| **Dataset** | Resume Dataset (26 curated candidates · 6 categories) |
| **Difficulty** | Intermediate |
| **Expected Outcome** | Faster candidate screening |

---

## ✨ Features

- **Multi-format resume parsing** — PDF (pdfplumber + PyPDF2 fallback), DOCX, TXT
- **NLP preprocessing pipeline** — spaCy tokenization, stopword removal, lemmatization
- **Skill extraction** — 250+ skill taxonomy across 13 domains via PhraseMatcher
- **Hybrid AI ranking** — TF-IDF cosine similarity + skill overlap ratio (adjustable weights)
- **Explainable results** — matched skills, missing skills, top TF-IDF keywords per candidate
- **4 sample job descriptions** — Data Scientist, Full-Stack Dev, HR Manager, Product Manager
- **Interactive visualizations** — ranked table, bar chart, candidate breakdown cards
- **CSV export** — one-click download of all results
- **100% offline** — no external APIs, no internet required after install

---

## 🚀 Quick Start

### Prerequisites
- Python 3.10 or higher
- pip

### 1. Clone the Repository

```bash
git clone https://github.com/<your-username>/resume-rank-pro.git
cd resume-rank-pro
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

> The spaCy `en_core_web_sm` model is included as a direct wheel URL in `requirements.txt` — **no separate download step needed**.

### 3. Run the App

```bash
streamlit run app.py
```

Open your browser at **http://localhost:8501**

---

## ☁️ Deploy to Streamlit Cloud

### Step 1 — Push to GitHub

```bash
git init
git add .
git commit -m "feat: initial RecruitIQ release"
git branch -M main
git remote add origin https://github.com/<your-username>/resume-rank-pro.git
git push -u origin main
```

### Step 2 — Deploy on Streamlit Community Cloud (free)

1. Go to [share.streamlit.io](https://share.streamlit.io) and sign in with GitHub.
2. Click **"New app"**.
3. Select your repository and branch (`main`).
4. Set **Main file path** to `app.py`.
5. Click **"Deploy"** — Streamlit Cloud automatically installs everything from `requirements.txt`.

> **No extra configuration needed.** The `en_core_web_sm` spaCy model is installed automatically via its wheel URL in `requirements.txt`.

### Step 3 — Share

Your app will be live at:
```
https://<your-username>-resume-rank-pro-app-<hash>.streamlit.app
```

---

## 🗂️ Project Structure

```
resume-rank-pro/
│
├── app.py                     # Streamlit application (main entry point)
├── requirements.txt           # All Python dependencies + spaCy model wheel
├── .gitignore                 # Files excluded from version control
├── README.md                  # This file
│
├── .streamlit/
│   └── config.toml            # Streamlit theme & server config
│
├── src/                       # Modular NLP & ranking pipeline
│   ├── __init__.py
│   ├── extractor.py           # PDF / DOCX / TXT text extraction
│   ├── preprocessor.py        # spaCy NLP: clean → tokenize → lemmatize
│   ├── skills.py              # 250+ skill taxonomy + PhraseMatcher extraction
│   ├── ranker.py              # TF-IDF scoring + composite ranking engine
│   └── sample_data.py         # Sample job descriptions + dataset loader
│
└── data/
    └── sample_resumes.csv     # 26 curated candidate resumes (6 categories)
```

---

## 🧠 How the Ranking Algorithm Works

### Pipeline Overview

```
Resume Files (PDF/DOCX/TXT)
        │
        ▼  src/extractor.py
   Raw Text Extraction
        │
        ▼  src/preprocessor.py  (spaCy)
   Clean → Tokenize → Remove Stopwords → Lemmatize
        │
        ├──────────────────────────────────────────┐
        ▼  src/skills.py                           ▼  src/ranker.py
   PhraseMatcher Skill Extraction          TF-IDF Vectorization
   (250+ skill taxonomy)                   (bigrams, 10K vocab)
        │                                          │
        ▼                                          ▼
   Skill Overlap Ratio                    Cosine Similarity
   matched / required                     JD vector · Resume vector
        │                                          │
        └──────────────┬───────────────────────────┘
                       ▼
            Composite Score = 0.70 × TF-IDF + 0.30 × Skill Overlap
                       │
                       ▼
             Ranked Results (descending)
```

### Scoring Formula

$$\text{Final Score} = (w_1 \times \text{TF-IDF Similarity}) + (w_2 \times \text{Skill Overlap Ratio})$$

Default weights: **70% TF-IDF + 30% Skill Match** (adjustable via sidebar slider)

### TF-IDF Configuration

```python
TfidfVectorizer(
    ngram_range=(1, 2),     # Captures bigrams: "machine learning", "deep learning"
    max_features=10_000,    # Cap vocabulary for performance
    sublinear_tf=True,      # Apply log(1+tf) — smooths term weighting
    min_df=1,
)
```

### Skill Taxonomy (13 Domains)

| Domain | Example Skills |
|---|---|
| Programming Languages | Python, Java, JavaScript, R, Go, Rust |
| Data Science & ML | Machine Learning, TensorFlow, PyTorch, scikit-learn |
| Web Development | React, Node.js, Django, REST API, Docker |
| Databases | SQL, PostgreSQL, MongoDB, Elasticsearch |
| Cloud & DevOps | AWS, Azure, GCP, Kubernetes, CI/CD |
| Human Resources | Recruitment, Talent Acquisition, Workday, HRIS |
| Project Management | Agile, Scrum, Jira, PMP, OKR |
| Marketing | SEO, Google Ads, HubSpot, Content Marketing |
| Finance | Financial Modeling, CFA, GAAP, Forecasting |
| Soft Skills | Leadership, Communication, Problem Solving |
| Testing & QA | Selenium, pytest, Jest, Test Automation |
| Cybersecurity | Penetration Testing, SIEM, ISO 27001 |
| Data Engineering | Apache Spark, Kafka, Airflow, dbt, Snowflake |

---

## 🖥️ UI Overview

| Section | Description |
|---|---|
| **Top Nav** | Brand bar with dataset/algorithm info |
| **Job Description Panel** | Paste custom JD or select from 4 sample roles |
| **Resume Source** | Upload PDF/DOCX/TXT files OR use built-in sample dataset |
| **Algorithm Weights** | Sidebar slider: adjust TF-IDF vs Skill Match contribution |
| **KPI Cards** | Candidates ranked, top score, avg score, JD skills count |
| **Ranked Table** | Colour-coded score table (green ≥60%, amber 30-60%, red <30%) |
| **Bar Chart** | Horizontal match score visualization across all candidates |
| **Skill Breakdown** | Expandable per-candidate view: matched / missing / extra skills |
| **CSV Download** | Export full ranked results instantly |

---

## 📦 Dependencies

| Package | Purpose |
|---|---|
| `streamlit` | Web UI framework |
| `spacy` + `en_core_web_sm` | NLP pipeline + PhraseMatcher |
| `scikit-learn` | TF-IDF vectorizer + cosine similarity |
| `pandas` | Data manipulation + CSV export |
| `pdfplumber` | Primary PDF text extraction |
| `PyPDF2` | Fallback PDF extraction |
| `python-docx` | DOCX text extraction |
| `matplotlib` | Bar chart visualization |
| `numpy` | Numerical operations |

---

## ⚙️ Configuration

### Streamlit Theme (`.streamlit/config.toml`)

```toml
[theme]
base                     = "dark"
primaryColor             = "#7c3aed"
backgroundColor          = "#07090f"
secondaryBackgroundColor = "#0d1117"
textColor                = "#f8fafc"
```

### Algorithm Weights

Adjust the **TF-IDF Similarity Weight** slider in the sidebar (0–100%):
- `1.0` = pure text similarity matching
- `0.0` = pure skill taxonomy matching
- `0.7` = default (recommended)

---

## 🔧 Troubleshooting

| Problem | Solution |
|---|---|
| `ModuleNotFoundError: spacy` | Run `pip install -r requirements.txt` |
| spaCy model not found | Already in `requirements.txt` as wheel URL — reinstall |
| PDF shows empty text | PDF may be image-only (scanned). Convert to TXT first |
| Streamlit not found | Run `pip install streamlit` |
| App won't start on Streamlit Cloud | Check repo has `requirements.txt` and `app.py` at root |

---

## 📄 License

MIT License — free to use, modify, and distribute for academic and commercial purposes.

---

<div align="center">
Built with Python · spaCy · scikit-learn · Streamlit
</div>
