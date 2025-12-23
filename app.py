import streamlit as st
import json
from openai import OpenAI

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="Smart Maths Learning", layout="centered")
st.title("📘 Smart Maths Learning (Class 7) for Ranbeer")

# ---------------- OPENAI CLIENT ----------------
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# ---------------- SESSION STATE ----------------
if "question_data" not in st.session_state:
    st.session_state.question_data = None
    st.session_state.answered = False
    st.session_state.correct = 0
    st.session_state.wrong = 0
    st.session_state.total = 0

# ---------------- CHAPTER SELECT ----------------
chapter = st.selectbox(
    "📚 Select Chapter",
    [
        "Integers",
        "Fractions and Decimals",
        "Simple Equations",
        "Lines and Angles",
        "Perimeter and Area"
    ]
)

# ---------------- AI QUESTION GENERATOR ----------------
def generate_question(chapter):
    prompt = f"""
You are a friendly Class 7 Maths teacher.

Create ONE multiple-choice question.

Rules:
- Ask the question FIRST
- 4 options (A, B, C, D)
- One correct answer
- Concept explanation AFTER answering
- Concept explanation must be ONE PARAGRAPH
- Language suitable for a 12-year-old
- Include visual/story-like explanation inside the paragraph

Return ONLY valid JSON.

JSON FORMAT:
{{
  "question": "",
  "options": {{
    "A": "",
    "B": "",
    "C": "",
    "D": ""
  }},
  "correct_option": "",
  "concept_explanation": "",
  "correct_feedback": "",
  "wrong_feedback": {{
    "hint": "",
    "example": ""
  }}
}}
"""

    response = client.responses.create(
        model="gpt-4.1-mini",
        input=prompt
    )

    return json.loads(response.output_text)

# ---------------- AUTO LOAD FIRST QUESTION ----------------
if st.session_state.question_data is None:
    st.session_state.question_data = generate_question(chapter)

data = st.session_state.question_data

# ---------------- DISPLAY QUESTION ----------------
st.subheader("❓ Question")
st.write(data["question"])

selected = st.radio(
    "Choose your answer:",
    options=list(data["options"].keys()),
    format_func=lambda x: f"{x}. {data['options'][x]}"
)

# ---------------- CHECK ANSWER ----------------
if st.button("✅ Check Answer") and not st.session_state.answered:
    st.session_state.answered = True
    st.session_state.total += 1

    if selected == data["correct_option"]:
        st.session_state.correct += 1
        st.success("🎉 " + data["correct_feedback"])
    else:
        st.session_state.wrong += 1
        st.error("❌ That's okay, learning happens here!")
        st.info("💡 Hint: " + data["wrong_feedback"]["hint"])
        st.info("✏️ Example: " + data["wrong_feedback"]["example"])

    st.divider()
    st.subheader("📘 Concept Explanation")
    st.write(data["concept_explanation"])

# ---------------- NEXT QUESTION ----------------
if st.session_state.answered:
    if st.button("➡️ Next Question"):
        st.session_state.question_data = generate_question(chapter)
        st.session_state.answered = False

# ---------------- REPORT CARD ----------------
st.divider()
if st.button("📄 Generate Report Card"):
    accuracy = (
        (st.session_state.correct / st.session_state.total) * 100
        if st.session_state.total > 0 else 0
    )

    st.subheader("📊 Report Card")
    st.write(f"📘 Total Questions: {st.session_state.total}")
    st.write(f"✅ Correct Answers: {st.session_state.correct}")
    st.write(f"❌ Wrong Answers: {st.session_state.wrong}")
    st.write(f"🎯 Accuracy: {accuracy:.1f}%")

    if accuracy >= 80:
        st.success("🌟 Excellent work! Keep it up!")
    elif accuracy >= 50:
        st.info("👍 Good progress! Practice a bit more.")
    else:
        st.warning("💪 Don't worry! Learning takes time.")
