import streamlit as st
from openai import OpenAI

# ---------------- PAGE SETUP ----------------
st.set_page_config(page_title="Class 7 Maths Question Generator", layout="wide")

st.title("📘 Class 7 Maths – Question Paper Generator")
st.write("Practice questions with **hidden answers** so students can try first.")

# ---------------- API KEY ----------------
api_key = None

if "OPENAI_API_KEY" in st.secrets:
    api_key = st.secrets["OPENAI_API_KEY"]
else:
    api_key = st.text_input("Enter OpenAI API Key", type="password")

if not api_key:
    st.warning("Please enter your OpenAI API key to continue.")
    st.stop()

client = OpenAI(api_key=api_key)

# ---------------- UI ----------------
chapter = st.selectbox(
    "Select Chapter",
    [
        "Integers",
        "Fractions and Decimals",
        "Algebraic Expressions",
        "Simple Equations",
        "Lines and Angles"
    ]
)

generate = st.button("Generate Question Paper")

# ---------------- AI LOGIC ----------------
def generate_paper(chapter):
    prompt = f"""
You are a friendly Class 7 Maths teacher.

Create ONE multiple-choice question for a 12-year-old student.

Chapter: {chapter}

Rules:
- Do NOT show the correct answer directly
- Use very simple language
- Make wrong options based on common mistakes

Return ONLY valid JSON. No extra text.

JSON format:
{{
  "question": "",
  "options": {{
    "A": "",
    "B": "",
    "C": "",
    "D": ""
  }},
  "correct_option": "",
  "correct_feedback": "",
  "wrong_feedback": {{
    "hint": "",
    "concept": "",
    "analogy": "",
    "example": ""
  }}
}}
"""


    response = client.responses.create(
        model="gpt-4.1-mini",
        input=prompt
    )

    return response.output_text

# ---------------- OUTPUT ----------------
if generate:
    with st.spinner("Creating question paper..."):
        content = generate_paper(chapter)

    st.subheader("📝 Question Paper")

    questions = content.split("Question")

    for i, q in enumerate(questions):
        if q.strip():
            st.markdown(f"### Question {i}")
            parts = q.split("Final Answer")

            st.write(parts[0])

            with st.expander("👉 Click to view Answer & Explanation"):
                if len(parts) > 1:
                    st.write("Final Answer" + parts[1])
