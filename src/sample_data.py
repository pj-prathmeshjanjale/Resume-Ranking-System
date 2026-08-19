"""
sample_data.py — Sample Job Descriptions & Dataset Loader
===========================================================
Provides:
  1. Pre-written sample job descriptions for demo purposes.
  2. A loader for the bundled sample_resumes.csv dataset.
"""

from __future__ import annotations
import logging
import os
import pandas as pd

logger = logging.getLogger(__name__)

# Path to the bundled sample dataset (relative to project root)
_DATASET_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "sample_resumes.csv")


# ══════════════════════════════════════════════════════════════════════════════
# SAMPLE JOB DESCRIPTIONS
# 4 realistic JDs covering the main categories in the resume dataset
# ══════════════════════════════════════════════════════════════════════════════

SAMPLE_JOB_DESCRIPTIONS: dict[str, str] = {

    "Data Scientist / ML Engineer": """
We are looking for an experienced Data Scientist to join our AI team.

Responsibilities:
- Design, build, and deploy machine learning and deep learning models.
- Perform exploratory data analysis and statistical modeling.
- Work with large datasets using Python, pandas, and NumPy.
- Develop NLP pipelines for text classification and information extraction.
- Collaborate with data engineers to build scalable ETL pipelines.
- Present insights to stakeholders using data visualizations.

Required Skills:
- Proficiency in Python, scikit-learn, TensorFlow or PyTorch.
- Strong knowledge of machine learning, deep learning, and NLP.
- Experience with SQL and NoSQL databases (PostgreSQL, MongoDB).
- Familiarity with cloud platforms: AWS, Azure, or GCP.
- Experience with data visualization tools: Matplotlib, Seaborn, Plotly, Tableau.
- Knowledge of Apache Spark or Hadoop is a plus.
- Version control using Git and GitHub.
- Experience with Docker and Kubernetes for model deployment.
- Strong statistical analysis and feature engineering skills.
- Communication and presentation skills.

Qualifications:
- Bachelor's or Master's degree in Computer Science, Statistics, or related field.
- 2+ years of experience in a data science or machine learning role.
""",

    "Full-Stack Web Developer": """
We are hiring a skilled Full-Stack Web Developer to build and maintain modern web applications.

Responsibilities:
- Develop responsive, high-performance web applications using React and Node.js.
- Design and implement RESTful APIs and GraphQL endpoints.
- Build and maintain relational and NoSQL databases (PostgreSQL, MongoDB).
- Write clean, well-documented code with unit and integration tests.
- Collaborate with UX/UI designers to implement pixel-perfect interfaces.
- Deploy and manage applications on AWS or Azure cloud infrastructure.
- Participate in code reviews and Agile sprint planning.

Required Skills:
- Proficiency in JavaScript, TypeScript, React.js, and Node.js.
- Experience with HTML5, CSS3, and modern CSS frameworks (Bootstrap, Tailwind).
- Backend development with Express.js or Django.
- Database design with PostgreSQL, MySQL, or MongoDB.
- RESTful API design and GraphQL.
- Version control with Git and GitHub.
- Docker and CI/CD pipelines.
- Agile/Scrum development methodology.
- Testing frameworks: Jest, Cypress, or Selenium.

Qualifications:
- Bachelor's degree in Computer Science or equivalent experience.
- 2+ years of full-stack web development experience.
""",

    "HR Manager": """
We are seeking an experienced HR Manager to lead our Human Resources department.

Responsibilities:
- Oversee full-cycle recruitment and talent acquisition for all departments.
- Design and implement employee onboarding programs.
- Manage compensation, benefits, and payroll administration.
- Lead performance management and succession planning initiatives.
- Develop and deliver training and learning & development programs.
- Ensure compliance with employment law and labor relations.
- Drive diversity, equity, and inclusion (DEI) programs.
- Use HR analytics and people analytics to inform workforce planning.
- Resolve employee relations conflicts and conduct investigations.
- Manage HRIS systems including Workday, BambooHR, or SuccessFactors.

Required Skills:
- Deep knowledge of recruitment, talent acquisition, and applicant tracking systems (ATS).
- Experience with performance management, compensation, and benefits.
- Strong knowledge of employment law and labor relations.
- Proficiency in Workday, BambooHR, SuccessFactors, or similar HRIS.
- HR analytics and people analytics capabilities.
- Change management and organizational development skills.
- Excellent communication, leadership, and conflict resolution skills.
- Experience with diversity and inclusion programs.

Qualifications:
- Bachelor's degree in Human Resources, Business Administration, or related field.
- 5+ years of progressive HR experience.
- SHRM-CP or PHR certification preferred.
""",

    "Product Manager": """
We are looking for a dynamic Product Manager to own the roadmap for our SaaS platform.

Responsibilities:
- Define and execute the product roadmap aligned with business strategy.
- Gather and prioritize customer requirements through user research and data analysis.
- Work closely with engineering, design, and marketing teams.
- Write detailed user stories and manage the product backlog in Jira.
- Track KPIs and OKRs to measure product success.
- Conduct A/B testing and analyze results to drive product decisions.
- Lead sprint planning, backlog grooming, and stakeholder communication.
- Manage product launches and go-to-market strategies.

Required Skills:
- Strong experience with Agile and Scrum methodologies.
- Proficiency in Jira and Confluence for backlog management.
- Data-driven decision making using analytics and A/B testing.
- Excellent stakeholder management and communication skills.
- Product roadmap planning and prioritization.
- Understanding of UX/UI design principles.
- Market research and competitive analysis.
- Business development and strategic thinking.
- KPI tracking and OKR frameworks.

Qualifications:
- Bachelor's degree in Business, Engineering, or related field.
- 3+ years of product management experience in a SaaS company.
- MBA or PMP certification is a plus.
""",
}


# ══════════════════════════════════════════════════════════════════════════════
# DATASET LOADER
# ══════════════════════════════════════════════════════════════════════════════

def load_sample_resumes(
    category_filter: str | None = None,
    max_per_category: int = 10,
) -> pd.DataFrame:
    """
    Load the bundled sample_resumes.csv dataset.

    Args:
        category_filter:  If given, filter to only this job category.
        max_per_category: Maximum number of resumes per category to return.

    Returns:
        DataFrame with columns: ['name', 'category', 'resume_text']
    """
    path = os.path.abspath(_DATASET_PATH)
    if not os.path.exists(path):
        logger.warning(f"Dataset not found at {path}.")
        return pd.DataFrame(columns=["name", "category", "resume_text"])

    df = pd.read_csv(path)

    # Normalise column names (case-insensitive)
    df.columns = [c.strip().lower() for c in df.columns]
    if "resume_text" not in df.columns and "resume" in df.columns:
        df.rename(columns={"resume": "resume_text"}, inplace=True)

    # Apply category filter
    if category_filter and "category" in df.columns:
        df = df[df["category"].str.lower() == category_filter.lower()]

    # Sample up to max_per_category from each category
    if "category" in df.columns:
        df = (
            df.groupby("category", group_keys=False)
            .apply(lambda g: g.sample(min(len(g), max_per_category), random_state=42))
            .reset_index(drop=True)
        )

    # Ensure required columns exist
    if "name" not in df.columns:
        df["name"] = [f"Candidate_{i+1}" for i in range(len(df))]
    if "category" not in df.columns:
        df["category"] = "Unknown"
    if "resume_text" not in df.columns:
        df["resume_text"] = ""

    return df[["name", "category", "resume_text"]].dropna(subset=["resume_text"])


def get_dataset_categories() -> list[str]:
    """Return sorted list of unique job categories in the dataset."""
    df = load_sample_resumes()
    if "category" in df.columns:
        return sorted(df["category"].unique().tolist())
    return []
