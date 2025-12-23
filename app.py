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

Create ONE multiple-choice question based on:
Chapter: {chapter}

Student age: 12 years

Rules:
- Do NOT show the correct answer directly
- Language must be very simple and encouraging
- Question must be syllabus-appropriate

Include the following:

1. Question
2. Four options (A, B, C, D)
   - One correct answer
   - Three incorrect answers based on common mistakes
3. Correct option letter (for internal use only)
4. Feedback if the student selects the WRONG answer:
   - A gentle hint (not the full answer)
   - Explain the concept in very easy language
   - Use a real-life analogy a 12-year-old can relate to
   - Give one small worked example
5. Feedback if the student selects the CORRECT answer:
   - One line of encouragement
   - One-line explanation why it is correct

IMPORTANT:
Return ONLY valid JSON in the exact format below.
Do not add any extra text.

{
  "question": "",
  "options": {
    "A": "",
    "B": "",
    "C": "",
    "D": ""
  },
  "correct_option": "",
  "correct_feedback": "",
  "wrong_feedback": {
    "hint": "",
    "concept": "",
    "analogy": "",
    "example": ""
  }
}
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
