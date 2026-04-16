# 📊 Job Eligibility & Role Fit Decision Engine

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-App-red.svg)
![AI](https://img.shields.io/badge/LLM-OpenAI%2FClaude-green.svg)
![Status](https://img.shields.io/badge/Status-Active-success.svg)

AI-powered decision system that evaluates job eligibility and role alignment for Intelligence, Fraud, Security, and Risk analytics positions.

The system combines rule-based classification with LLM-driven scoring to determine whether a candidate is truly qualified based on experience thresholds, role type alignment, and structured fit analysis.

---

## 🚀 What This Project Does

Job Fit Analyzer helps users:
- Evaluate how well they match a job posting
- Identify skill and experience gaps
- Generate resume improvement suggestions
- Provide apply vs. skip recommendations

It is designed for:
- Risk, fraud, and operations roles
- Federal job applications (DHS, FBI, intelligence roles)
- Career transition and resume optimization

---

## 🧠 Core Innovation

This system is not a generic resume optimizer.

It introduces a hybrid decision architecture:

- **Eligibility-first evaluation layer**
  - Enforces minimum requirements (years of experience, degree requirements)
  - Prevents inflated AI scoring for non-qualified roles

- **Role classification engine**
  - Identifies job type (Intelligence, Fraud, Risk, Investigations, Security Analysis)
  - Filters out non-target domains

- **LLM-assisted scoring layer**
  - Generates structured 0–100 fit score
  - Provides explainable reasoning ("why this score")
  - Outputs APPLY / SKIP decision logic

---

## 🧠 Key Features

### 🔍 Job Type Classification Engine
Classifies job postings into:
- Intelligence / Investigations
- Fraud & Risk Analytics
- Security Analysis
- Operations / Program Management

### 🧭 Eligibility Evaluation Layer
Evaluates strict job requirements:
- Years of experience thresholds
- Degree requirements
- Must-have qualifications

Prevents over-scoring in non-eligible roles.

### 📊 Hybrid Fit Scoring System
Combines:
- Rule-based classification signals
- LLM-generated evaluation
- Role alignment scoring

Outputs:
- 0–100 fit score
- Confidence level
- APPLY / SKIP decision

### 🧠 Explainable AI Output
Each result includes:
- Key strengths
- Key gaps
- Simplified rationale ("why this score")

### 📝 Resume Optimization Support
Generates:
- Improved resume bullets based on real experience
- Role-aligned phrasing for intelligence/risk roles

---

## 🛠 Tech Stack

- Python (Core engine) 🐍
- Streamlit (UI Layer) 📊
- OpenAI API (LLM reasoning layer) 🤖
- Rule-based classification engine
- JSON-config driven architecture
- Hybrid deterministic + probabilistic scoring model

---

## 📁 Project Structure

job-fit-analyzer/

│
├── app.py                 # Streamlit interface + orchestration layer
├── resume.json            # Structured candidate profile data
├── config.json            # Job classification + scoring rules engine
├── run_app.command        # Local execution launcher

│
├── core/
│   ├── classifier.py      # Job type classification logic
│   ├── scoring.py         # Fit scoring + decision logic
│   ├── eligibility.py     # Minimum requirement validation layer
│
└── README.md              # Project documentation


---



## ⚙️ How to Run

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

---

### 2. Run the app

```bash
streamlit run app.py
```

or

```bash
./run_app.command
```

---
## 🧪 Example Output

```json
{
  "fit_score": 82,
  "strengths": [
    "Strong operations and fraud detection experience",
    "Risk analysis background"
  ],
  "gaps": [
    "Limited OSINT tooling experience",
    "No formal clearance exposure"
  ],
  "recommendation": "Apply with resume tailoring"
}
```

---

## 🎯 Use Cases

- Security operations career alignment
- Intelligence & threat analysis role screening
- Fraud detection / risk analytics job evaluation
- Structured career positioning in regulated environments

---

## 🔮 Future Enhancements

- Multi-job batch evaluation engine
- Embedding-based semantic scoring layer
- Job board discovery scraping
- Job requirement decomposition (must-have vs nice-to-have)

---

## ⚠️ Disclaimer

This tool provides AI-generated guidance and should be used as a **decision support system**, not a hiring guarantee tool.

---

## 👤 Author

**Alex Champa**

Focus areas:
- Security analysis
- Risk & fraud analysis
- Intelligence, risk, and security analytics tooling
