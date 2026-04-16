# 📊 Job Fit Analyzer

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-App-red.svg)
![AI](https://img.shields.io/badge/LLM-OpenAI%2FClaude-green.svg)
![Status](https://img.shields.io/badge/Status-Active-success.svg)

AI-powered tool that analyzes job descriptions against a candidate profile and generates **fit scores, gap analysis, and resume tailoring recommendations**.

---

## 🚀 What This Project Does

Job Fit Analyzer helps users:
- Evaluate how well they match a job posting
- Identify skill and experience gaps
- Generate resume improvement suggestions
- Provide apply vs. skip recommendations

It is designed for:
- Federal job applications (DHS, FBI, intelligence roles)
- Risk, fraud, and operations roles
- Career transition and resume optimization

---

## 🧠 Key Features

### 🔍 Job Description Analysis
Extracts:
- Skills
- Responsibilities
- Qualifications
- Keywords (ATS optimization)

### 📊 Fit Scoring Engine
Computes a structured match score based on:
- Skills alignment
- Experience relevance
- Domain overlap
- Role seniority match

### 🧠 Gap Analysis
Identifies:
- Missing skills
- Weak experience areas
- Suggested improvements

### 📝 Resume Tailoring
Generates:
- Optimized bullet points
- Keyword-aligned phrasing
- Role-specific resume improvements

### 🧭 Application Strategy
Provides:
- Apply vs. skip recommendation
- Focus areas for interview prep
- Optional certification suggestions

---

## 🛠 Tech Stack

- Python 🐍
- Streamlit 📊
- OpenAI API / Claude API 🤖
- JSON-based data structure
- LLM prompt engineering

---

## 📁 Project Structure

job-fit-analyzer/
│
├── app.py # Main application
├── resume.json # Candidate profile input
├── run_app.command # Quick launch script
├── README.md # Project documentation


---

## ⚙️ How to Run

### 1. Install dependencies
```bash
pip install -r requirements.txt

streamlit run app.py
OR 
./run_app.command

Example Output
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


🎯 Use Cases
Federal job applications (DHS, FBI, intelligence)
Risk & fraud operations roles
Resume optimization before applying
Career planning and transition strategy

🔮 Future Enhancements
Multi-resume comparison mode
Job tracking dashboard
Chrome extension (LinkedIn / USAJobs integration)
Export tailored resume (PDF/DOCX)
Multi-model support (GPT + Claude switching)

⚠️ Disclaimer

This tool provides AI-generated guidance and should be used as a decision support system, not a hiring guarantee tool.

👤 Author

Alex Champa

Focus areas:
Security analysis
Risk & fraud Analysis
AI-assisted career tooling