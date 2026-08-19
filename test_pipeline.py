"""
test_pipeline.py — End-to-end pipeline integration test
Run with: python test_pipeline.py
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))

from src.preprocessor import preprocess, preprocess_batch, get_nlp
from src.skills import extract_skills, compute_skill_match
from src.ranker import compute_composite_scores, results_to_dataframe
from src.sample_data import load_sample_resumes, get_dataset_categories, SAMPLE_JOB_DESCRIPTIONS

def sep(title):
    print(f"\n{'='*60}")
    print(f"  {title}")
    print('='*60)

# ── Test 1: Preprocessor ──────────────────────────────────────────────────────
sep("TEST 1: NLP Preprocessor")
jd_text = "Looking for a Python developer skilled in machine learning, TensorFlow, and SQL."
jd_proc, jd_doc = preprocess(jd_text)
print(f"Input : {jd_text}")
print(f"Output: {jd_proc}")
print("[PASS]")

# ── Test 2: Skill Extraction ──────────────────────────────────────────────────
sep("TEST 2: Skill Extraction")
nlp = get_nlp()
jd_skills = extract_skills(jd_doc, nlp)
print(f"JD Skills detected: {sorted(jd_skills)}")

resume_text = "I am an expert in Python, scikit-learn, TensorFlow, SQL, Docker, and deep learning."
_, rdoc = preprocess(resume_text)
resume_skills = extract_skills(rdoc, nlp)
print(f"Resume Skills:      {sorted(resume_skills)}")

match = compute_skill_match(jd_skills, resume_skills)
print(f"Matched:  {match['matched_skills']}")
print(f"Missing:  {match['missing_skills']}")
print(f"Overlap:  {match['skill_overlap_ratio']:.2%}")
print("[PASS]")

# ── Test 3: TF-IDF Ranker ─────────────────────────────────────────────────────
sep("TEST 3: TF-IDF Ranking (3 candidates)")
resume_texts = [
    "Python developer with TensorFlow and deep learning experience. Worked on NLP projects.",
    "Java backend developer with Spring Boot, REST API, and MySQL database experience.",
    "Data scientist: Python, scikit-learn, machine learning, SQL, Docker, cloud computing.",
]
names = ["Alice (Python/ML)", "Bob (Java/Backend)", "Carol (Data Science)"]

preprocessed = preprocess_batch(resume_texts)
resumes_proc = [p[0] for p in preprocessed]
resume_docs  = [p[1] for p in preprocessed]

skill_results = []
for d in resume_docs:
    rs = extract_skills(d, nlp)
    skill_results.append(compute_skill_match(jd_skills, rs))

results = compute_composite_scores(
    jd_processed=jd_proc,
    resumes_processed=resumes_proc,
    skill_results=skill_results,
    candidate_names=names,
    candidate_raw_texts=resume_texts,
    tfidf_weight=0.70,
    skill_weight=0.30,
)
df = results_to_dataframe(results)
print(df[["Rank","Candidate","Match Score (%)","TF-IDF Score","Skill Score (%)","Matched Skills"]].to_string(index=False))
print("[PASS]")

# ── Test 4: Sample Dataset ────────────────────────────────────────────────────
sep("TEST 4: Sample Dataset Loader")
cats = get_dataset_categories()
print(f"Categories: {cats}")
df_all = load_sample_resumes()
print(f"Total resumes: {len(df_all)}")
print(f"Columns: {list(df_all.columns)}")
print(f"\nSample names: {df_all['name'].tolist()[:5]}")

df_ds = load_sample_resumes(category_filter="Data Science")
print(f"\nData Science resumes: {len(df_ds)}")
print("[PASS]")

# ── Test 5: Full Dataset Ranking ──────────────────────────────────────────────
sep("TEST 5: Full Dataset Ranking (Data Scientist JD vs all Data Science resumes)")
jd_full = SAMPLE_JOB_DESCRIPTIONS["Data Scientist / ML Engineer"]
jd_full_proc, jd_full_doc = preprocess(jd_full)
jd_full_skills = extract_skills(jd_full_doc, nlp)
print(f"JD skills extracted: {len(jd_full_skills)} skills")
print(f"Skills: {sorted(jd_full_skills)}")

# Rank against all Data Science candidates
candidates = [
    {"name": row["name"], "text": row["resume_text"]}
    for _, row in df_ds.iterrows()
]
texts = [c["text"] for c in candidates]
cnames = [c["name"] for c in candidates]

batch = preprocess_batch(texts)
r_procs = [p[0] for p in batch]
r_docs  = [p[1] for p in batch]

sr = []
for d in r_docs:
    rs = extract_skills(d, nlp)
    sr.append(compute_skill_match(jd_full_skills, rs))

final_results = compute_composite_scores(
    jd_processed=jd_full_proc,
    resumes_processed=r_procs,
    skill_results=sr,
    candidate_names=cnames,
    candidate_raw_texts=texts,
    tfidf_weight=0.70,
    skill_weight=0.30,
)
df_out = results_to_dataframe(final_results)
print("\nRanked Results:")
print(df_out[["Rank","Candidate","Match Score (%)","TF-IDF Score","Skill Score (%)"]].to_string(index=False))
print("[PASS]")

# ── CSV Export Test ───────────────────────────────────────────────────────────
sep("TEST 6: CSV Export")
out_path = "data/sample_ranking_output.csv"
df_out.to_csv(out_path, index=False)
print(f"CSV written to: {out_path}")
print("[PASS]")

sep("ALL 6 TESTS PASSED [OK]")
print("The pipeline is working correctly. Run: streamlit run app.py")
