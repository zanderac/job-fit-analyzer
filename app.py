import streamlit as st
from openai import OpenAI
import json
import os

# ----------------------
# OpenAI Client
# ----------------------
client = OpenAI("INSERT_API_KEY_HERE")

st.set_page_config(page_title="Job Fit Analyzer", layout="wide")

st.title("Job Fit Analyzer (Dual Mode Engine)")

st.markdown("""
Analyze job fit and optimize your resume.

Modes:
- 🟢 Safe Rewrite (Application Mode)
- 🟡 Gap Bridge (Planning Mode)
""")

# ----------------------
# Mode Selector
# ----------------------
mode = st.radio(
    "Select Mode",
    ["Safe Rewrite (Apply Mode)", "Gap Bridge (Planning Mode)"]
)

# ----------------------
# Load Resume
# ----------------------
BASE_DIR = os.path.dirname(__file__)

def load_resume():
    path = os.path.join(BASE_DIR, "resume.json")
    with open(path, "r") as f:
        return json.load(f)

resume_json = load_resume()

# ----------------------
# Job Input
# ----------------------
st.subheader("Job Description")

jd_input = st.text_area(
    "Paste job description here",
    height=300
)

# ----------------------
# Prompt Builder
# ----------------------
def build_prompt(resume, job, mode):

    if mode == "Safe Rewrite (Apply Mode)":

        return f"""
You are a strict job fit evaluator and resume rewrite engine.

MODE: SAFE REWRITE (APPLICATION MODE)

TASK:
1. Decide APPLY or SKIP
2. Score job fit (0–100)
3. Identify strengths and gaps
4. Rewrite ONLY existing resume experience into improved bullets

Return structured output following schema exactly.

RULES:
- ONLY use real experience from resume
- DO NOT invent new work
- Must include action + tool + impact where possible
- Keep output concise and job-aligned

RESUME:
{json.dumps(resume, indent=2)}

JOB:
{job}
"""

    else:

        return f"""
You are a career strategy and skill gap analysis engine.

MODE: GAP BRIDGE (PLANNING MODE)

TASK:
1. Identify missing skills and experience gaps
2. Identify what blocks candidacy
3. Suggest future resume bullets (clearly hypothetical)

Return structured output following schema exactly.

RULES:
- Future bullets are NOT real experience
- Clearly represent skills to build toward
- Focus on fraud, risk, intelligence, investigations

RESUME:
{json.dumps(resume, indent=2)}

JOB:
{job}
"""

# ----------------------
# Run Analysis
# ----------------------
if st.button("Analyze Fit"):

    if not jd_input:
        st.error("Please paste a job description.")
        st.stop()

    prompt = build_prompt(resume_json, jd_input, mode)

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            temperature=0,
            messages=[
                {"role": "user", "content": prompt}
            ],
            response_format={
                "type": "json_schema",
                "json_schema": {
                    "name": "job_fit_engine",
                    "schema": {
                        "type": "object",
                        "properties": {
                            "mode": {"type": "string"},

                            "decision": {
                                "type": "string",
                                "enum": ["APPLY", "SKIP"]
                            },

                            "score": {"type": "number"},
                            "confidence": {
                                "type": "string",
                                "enum": ["HIGH", "MEDIUM", "LOW"]
                            },

                            "fit_drivers": {
                                "type": "object",
                                "properties": {
                                    "strengths": {
                                        "type": "array",
                                        "items": {"type": "string"}
                                    },
                                    "gaps": {
                                        "type": "array",
                                        "items": {"type": "string"}
                                    }
                                },
                                "required": ["strengths", "gaps"]
                            },

                            "resume_bullet_rewrites": {
                                "type": "array",
                                "items": {"type": "string"}
                            },

                            "missing_skills": {
                                "type": "array",
                                "items": {"type": "string"}
                            },

                            "career_gaps": {
                                "type": "array",
                                "items": {"type": "string"}
                            },

                            "future_resume_bullets": {
                                "type": "array",
                                "items": {"type": "string"}
                            }
                        },
                        "required": ["mode"]
                    }
                }
            }
        )

        output = json.loads(response.choices[0].message.content)

        # ----------------------
        # UI OUTPUT
        # ----------------------
        st.subheader("Results")

        st.write(f"Mode: {output.get('mode')}")

        # ----------------------
        # SAFE REWRITE MODE
        # ----------------------
        if output.get("mode") == "Safe Rewrite (Apply Mode)" or output.get("resume_bullet_rewrites"):

            st.subheader("Decision")

            if output.get("decision") == "APPLY":
                st.success("APPLY")
            else:
                st.error("SKIP")

            st.write(f"Score: {output.get('score')}")
            st.write(f"Confidence: {output.get('confidence')}")

            col1, col2 = st.columns(2)

            with col1:
                st.subheader("Strengths")
                st.write(output["fit_drivers"]["strengths"])

                st.subheader("Resume Bullet Rewrites")
                st.write(output.get("resume_bullet_rewrites", []))

            with col2:
                st.subheader("Gaps")
                st.write(output["fit_drivers"]["gaps"])

        # ----------------------
        # GAP BRIDGE MODE
        # ----------------------
        else:

            st.subheader("Missing Skills")
            st.write(output.get("missing_skills", []))

            st.subheader("Career Gaps")
            st.write(output.get("career_gaps", []))

            st.subheader("Future Resume Bullets (Planning Only)")
            st.write(output.get("future_resume_bullets", []))

    except Exception as e:
        st.error(f"Error: {str(e)}")
