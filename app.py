import streamlit as st
import openai

st.set_page_config(page_title="Class 7 Maths Question Generator", layout="wide")

st.title("📘 Class 7 Maths – Question Paper Generator")
st.write("Practice questions with **hidden answers** so students can try first.")

# API key
openai.api_key = st.secrets["OPENAI_API_KEY"]

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

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )

    return response.choices[0].message.content


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
