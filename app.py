import streamlit as st
import json
from openai import OpenAI

# ------------------ CONFIG ------------------
st.set_page_config(page_title="Class 7 Maths Practice", layout="centered")
st.title("📘 Class 7 Maths – Smart Practice")

# ------------------ OPENAI CLIENT ------------------
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# ------------------ USER INPUT ------------------
chapter = st.selectbox(
    "Select Chapter",
    [
        "Integers",
        "Fractions and Decimals",
        "Simple Equations",
        "Lines and Angles",
        "Perimeter and Area"
    ]
)

# ------------------ AI LOGIC ------------------
def generate_question(chapter):
    prompt = f"""
You are a friendly Class 7 Maths teacher.

Create ONE multiple-choice question for a 12-year-old student.

Chapter: {chapter}

Rules:
- Do NOT show the correct answer directly
- Use very simple language
- Wrong options should reflect common mistakes
- Make learning gentle and encouraging

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

    return json.loads(response.output_text)

# ------------------ UI LOGIC ------------------
if "question_data" not in st.session_state:
    st.session_state.question_data = None
    st.session_state.answered = False

if st.button("Generate Question"):
    st.session_state.question_data = generate_question(chapter)
    st.session_state.answered = False

# ------------------ DISPLAY QUESTION ------------------
if st.session_state.question_data:
    data = st.session_state.question_data

    st.subheader("🧠 Question")
    st.write(data["question"])

    selected = st.radio(
        "Choose your answer:",
        options=list(data["options"].keys()),
        format_func=lambda x: f"{x}. {data['options'][x]}"
    )

    if st.button("Check Answer"):
        st.session_state.answered = True

        if selected == data["correct_option"]:
            st.success("✅ " + data["correct_feedback"])
        else:
            st.error("❌ Not quite. Let’s understand it better 👇")
            st.info("💡 Hint: " + data["wrong_feedback"]["hint"])
            st.info("📘 Concept: " + data["wrong_feedback"]["concept"])
            st.info("🧠 Analogy: " + data["wrong_feedback"]["analogy"])
            st.info("✏️ Example: " + data["wrong_feedback"]["example"])

    if st.session_state.answered:
        st.button("Next Question", on_click=lambda: st.session_state.update(
            {"question_data": None, "answered": False}
        ))
