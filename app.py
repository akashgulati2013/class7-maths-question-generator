import streamlit as st
from openai import OpenAI

# ---------- CONFIG ----------
st.set_page_config(page_title="Class 7 Maths Question Generator", layout="wide")

st.title("📘 Class 7 Maths – Question Paper Generator")
st.write("Practice questions with **hidden answers** so students can try first.")

# ---------- INPUTS ----------
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

# ---------- AI CLIENT ----------
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# ---------- PROMPT ----------
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
- Avoid textbook copying

For EACH question provide:
1. Question
2. Final Answer
3. Step-by-step Explanation (simple language)
4. Concept Used
5. Related Concepts

Format neatly.
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )

    return response.choices[0].message.content

# ---------- OUTPUT ----------
if generate:
    with st.spinner("Creating question paper..."):
        content = generate_paper(chapter)

    st.subheader("📝 Question Paper")

    sections = content.split("Question")

    for i, section in enumerate(sections):
        if section.strip():
            st.markdown(f"### Question {i}")
            parts = section.split("Final Answer")

            # Question text
            st.write(parts[0])

            # Hidden answer
            with st.expander("👉 Click to view Answer & Explanation"):
                st.write("Final Answer" + parts[1])
