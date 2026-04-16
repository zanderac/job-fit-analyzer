import streamlit as st
from openai import OpenAI
import json
import os

# ----------------------
# OPENAI CLIENT
# ----------------------
client = OpenAI()

st.set_page_config(page_title="Job Fit Analyzer", layout="wide")

st.title("Job Fit Analyzer (Eligibility + Fit Engine)")

st.markdown("""
Evaluates job eligibility + fit for Intelligence, Fraud, Investigations, Security Analysis, and Risk roles.
""")

# ----------------------
# LOAD FILES
# ----------------------
BASE_DIR = os.path.dirname(__file__)

def load_resume():
    path = os.path.join(BASE_DIR, "resume.json")
    with open(path, "r") as f:
        return json.load(f)

def load_config():
    path = os.path.join(BASE_DIR, "config.json")
    with open(path, "r") as f:
        return json.load(f)

resume_json = load_resume()
config = load_config()

# ----------------------
# INPUT
# ----------------------
st.subheader("Job Description")

jd_input = st.text_area("Paste job description here", height=300)

# ----------------------
# JOB TYPE CLASSIFIER
# ----------------------
def classify_job(job_text, config):
    text = job_text.lower()

    best_match = None
    best_score = 0

    for job_type, data in config["job_fit_layer"]["job_type_definitions"].items():
        score = 0
        for keyword in data["keywords"]:
            if keyword.lower() in text:
                score += 1

        if score > best_score:
            best_score = score
            best_match = job_type

    return best_match

# ----------------------
# TITLE-ONLY EXCLUSION (SAFE)
# ----------------------
def extract_title(job_text):
    return job_text[:200].lower()

def is_hard_exclusion(job_text, config):
    title_section = extract_title(job_text)
    excluded_titles = config["job_fit_layer"]["hard_exclusions"]["titles"]

    return any(title in title_section for title in excluded_titles)

# ----------------------
# FIT CLASS
# ----------------------
def get_fit_class(score):
    rules = config["job_fit_layer"]["fit_class_rules"]

    if score >= rules["Strong"]["min_score"]:
        return "Strong"
    elif score >= rules["Medium"]["min_score"]:
        return "Medium"
    else:
        return "Weak"

# ----------------------
# PROMPT (ELIGIBILITY FIRST)
# ----------------------
def build_prompt(resume, job):
    return f"""
You are a job eligibility and fit evaluation engine.

STEP 1: ELIGIBILITY CHECK (STRICT)
Evaluate minimum qualifications:
- years of experience requirement
- degree requirement
- must-have skills

Return:
- eligibility_status: PASS / PARTIAL / FAIL
- eligibility_reason: short explanation

STEP 2: JOB TYPE CLASSIFICATION
Identify if role is aligned to:
fraud, risk, intelligence, investigations, or security analysis

STEP 3: FIT SCORE (0–100)
Only after eligibility step.

STEP 4: DECISION
Return APPLY or SKIP

STEP 5: WHY THIS SCORE (simple)
Return:
- key_match
- key_miss
- summary

RULES:
- Be strict on years of experience
- Do NOT inflate scores for FAIL eligibility
- Ignore engineering tools unless they define job title

RESUME:
{json.dumps(resume, indent=2)}

JOB:
{job}
"""

# ----------------------
# RUN ANALYSIS
# ----------------------
if st.button("Analyze Fit"):

    if not jd_input.strip():
        st.error("Please paste a job description.")
        st.stop()

    # ----------------------
    # HARD EXCLUSION CHECK
    # ----------------------
    if is_hard_exclusion(jd_input, config):
        st.error("🚫 Excluded Role (Engineering / Infrastructure Title Detected)")
        st.stop()

    # ----------------------
    # JOB TYPE
    # ----------------------
    job_type = classify_job(jd_input, config)

    # ----------------------
    # GPT CALL (SAFE WRAPPED)
    # ----------------------
    try:
        prompt = build_prompt(resume_json, jd_input)

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
                            "eligibility_status": {
                                "type": "string",
                                "enum": ["PASS", "PARTIAL", "FAIL"]
                            },
                            "eligibility_reason": {"type": "string"},
                            "decision": {
                                "type": "string",
                                "enum": ["APPLY", "SKIP"]
                            },
                            "score": {"type": "number"},
                            "why_this_score": {
                                "type": "object",
                                "properties": {
                                    "key_match": {"type": "string"},
                                    "key_miss": {"type": "string"},
                                    "summary": {"type": "string"}
                                },
                                "required": ["key_match", "key_miss", "summary"]
                            }
                        },
                        "required": [
                            "eligibility_status",
                            "eligibility_reason",
                            "decision",
                            "score",
                            "why_this_score"
                        ]
                    }
                }
            }
        )

        output = json.loads(response.choices[0].message.content)

        score = output.get("score", 0)
        fit_class = get_fit_class(score)

        # ----------------------
        # UI OUTPUT
        # ----------------------
        st.subheader("Job Fit Results")

        st.write(f"Job Type: {job_type}")
        st.write(f"Score: {score}")
        st.write(f"Fit Class: {fit_class}")

        st.divider()

        st.subheader("Eligibility Check")
        st.write(output["eligibility_status"])
        st.write(output["eligibility_reason"])

        st.divider()

        if output["decision"] == "APPLY":
            st.success("APPLY")
        else:
            st.error("SKIP")

        st.divider()

        st.subheader("Why This Score")

        st.write("Key Match:", output["why_this_score"]["key_match"])
        st.write("Key Miss:", output["why_this_score"]["key_miss"])
        st.write("Summary:", output["why_this_score"]["summary"])

    except Exception as e:
        st.error("Something went wrong during analysis.")
        st.exception(e)
