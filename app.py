import streamlit as st
import json
from openai import OpenAI

# ------------------ PAGE CONFIG ------------------
st.set_page_config(page_title="Class 7 Maths – Learn & Practice", layout="centered")
st.title("📘 Class 7 Maths – Learn & Practice Smartly")

# ------------------ OPENAI CLIENT ------------------
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# ------------------ USER INPUT ------------------
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

# ------------------ AI QUESTION GENERATOR ------------------
def generate_question(chapter):
    prompt = f"""
You are a friendly and creative Class 7 Maths teacher.

Create ONE multiple-choice question for a 12-year-old student.

Chapter: {chapter}

Teaching Style:
- Very simple language
- Bullet points
- Friendly, encouraging tone
- Think like a school teacher using cartoons and stories

IMPORTANT RULES:
- Do NOT reveal the correct answer directly
- Wrong options should be common student mistakes
- Help the child understand AND remember

Return ONLY valid JSON. No extra text.

JSON FORMAT:
{{
  "concept_explanation": {{
    "title": "",
    "bullets": [
      "",
      "",
      ""
    ],
    "cartoon_idea": ""
  }},
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

# ------------------ SESSION STATE ------------------
if "question_data" not in st.session_state:
    st.session_state.question_data = None
    st.session_state.answered = False

# ------------------ GENERATE QUESTION ------------------
if st.button("✨ Generate New Question"):
    st.session_state.question_data = generate_question(chapter)
    st.session_state.answered = False

# ------------------ DISPLAY QUESTION ------------------
if st.session_state.question_data:
    data = st.session_state.question_data

    # ---------- CONCEPT EXPLANATION ----------
    st.subheader("🧠 Concept to Remember")
    st.markdown(f"**{data['concept_explanation']['title']}**")

    for bullet in data["concept_explanation"]["bullets"]:
        st.markdown(f"- {bullet}")

    st.info("🎨 Imagine this like a cartoon:")
    st.write(data["concept_explanation"]["cartoon_idea"])

    st.divider()

    # ---------- QUESTION ----------
    st.subheader("❓ Question")
    st.write(data["question"])

    selected = st.radio(
        "Choose your answer:",
        options=list(data["options"].keys()),
        format_func=lambda x: f"{x}. {data['options'][x]}"
    )

    # ---------- CHECK ANSWER ----------
    if st.button("✅ Check Answer"):
        st.session_state.answered = True

        if selected == data["correct_option"]:
            st.success("🎉 " + data["correct_feedback"])
        else:
            st.error("❌ Not quite. Let’s learn it step by step 👇")
            st.info("💡 Hint: " + data["wrong_feedback"]["hint"])
            st.info("📘 Concept: " + data["wrong_feedback"]["concept"])
            st.info("🧠 Analogy: " + data["wrong_feedback"]["analogy"])
            st.info("✏️ Example: " + data["wrong_feedback"]["example"])

    # ---------- NEXT QUESTION ----------
    if st.session_state.answered:
        st.button(
            "➡️ Next Question",
            on_click=lambda: st.session_state.update(
                {"question_data": None, "answered": False}
            )
        )
