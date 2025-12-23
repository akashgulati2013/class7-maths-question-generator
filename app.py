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
You are a Class 7 Mathematics teacher.

Create a question paper for:
Chapter: {chapter}

Question mix:
- 5 easy
- 3 medium
- 2 application-based questions

Rules:
- Questions must be original
- Use simple Class 7 language

For EACH question provide:
1. Question
2. Final Answer
3. Step-by-step Explanation
4. Concept Used
5. Related Concepts
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
