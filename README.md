# RecruitIQ — AI-Based Resume Ranking System

<div align="center">

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://resume-ranking-system-pro.streamlit.app/)
![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=flat-square&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.32%2B-FF4B4B?style=flat-square&logo=streamlit&logoColor=white)
![spaCy](https://img.shields.io/badge/spaCy-3.8-09A3D5?style=flat-square&logo=spacy&logoColor=white)
![scikit-learn](https://img.shields.io/badge/scikit--learn-1.4%2B-F7931E?style=flat-square&logo=scikit-learn&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-22c55e?style=flat-square)

**An AI-powered resume screening tool that ranks candidate resumes against job descriptions using NLP, TF-IDF similarity, and a 250+ skill taxonomy.**

🌐 **Live Web App:** [https://resume-ranking-system-pro.streamlit.app/](https://resume-ranking-system-pro.streamlit.app/)

[🌐 Live Demo](https://resume-ranking-system-pro.streamlit.app/) · [🚀 Quick Start](#-quick-start) · [🧠 How It Works](#-how-the-ranking-algorithm-works) · [📋 Project Metadata](#-project-metadata)

</div>

---

## 🌐 Live Application

The application is deployed on Streamlit Community Cloud:

🔗 **[https://resume-ranking-system-pro.streamlit.app/](https://resume-ranking-system-pro.streamlit.app/)**

No installation needed — test job descriptions, rank sample resumes, or upload your own PDF/DOCX resumes directly in your browser.

---

## 📋 Project Metadata

| Field | Value |
|---|---|
| **Project ID** | P17 |
| **Title** | AI-Based Resume Ranking System |
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
- **Interactive visualizations** — ranked table, Altair vector chart, candidate breakdown cards
- **CSV export** — one-click download of all results
- **100% cloud & offline capable** — runs locally or hosted on Streamlit Cloud

---

## 🚀 Quick Start (Local Setup)

### Prerequisites
- Python 3.10 or higher
- pip

### 1. Clone the Repository

```bash
git clone https://github.com/pj-prathmeshjanjale/Resume-Ranking-System.git
cd Resume-Ranking-System
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

## ☁️ Deployment Details

The repository is configured for one-click deployment on Streamlit Community Cloud:

- **GitHub Repository:** `pj-prathmeshjanjale/Resume-Ranking-System`
- **Main Branch:** `main`
- **Main File:** `app.py`
- **Live URL:** `https://resume-ranking-system-pro.streamlit.app/`

---

## 🗂️ Project Structure

```
Resume-Ranking-System/
│
├── app.py                     # Streamlit application (main entry point)
├── requirements.txt           # Python dependencies + spaCy model wheel
├── .gitignore                 # Files excluded from version control
├── README.md                  # Detailed documentation & deployment guide
│
├── .streamlit/
│   └── config.toml            # Streamlit theme & server configuration
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

---

## 📄 License

MIT License — free to use, modify, and distribute for academic and commercial purposes.

---

<div align="center">
Built with Python · spaCy · scikit-learn · Streamlit
</div>
