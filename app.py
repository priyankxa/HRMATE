
import streamlit as st

from llm import create_llm
from rag import rag_chain
from tools import screen_resume, get_interview_slots


st.set_page_config(
    page_title="HRMATE AI",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 HRMATE")
st.subheader("Your AI Recruitment Assistant")
st.write(
    "Ask HR policy questions, screen resumes, "
    "and view available interview slots."
)

tab1, tab2, tab3 = st.tabs([
    "💬 HR Assistant",
    "📄 Resume Screening",
    "📅 Interview Slots"
])

with tab1:
    st.header("Ask an HR Question")

    question = st.text_input(
        "Enter your question",
        placeholder="What benefits does the company provide?"
    )

    if st.button("Get Answer"):
        if question.strip():
            with st.spinner("Searching company documents..."):
                try:
                    result = rag_chain(question)
                    st.write(result["result"])
                except Exception as e:
                    st.error(f"Could not get an answer: {e}")
        else:
            st.warning("Please enter a question.")

with tab2:
    st.header("Candidate Resume Screening")

    if st.button("Screen Candidate"):
        with st.spinner("Analyzing resume..."):
            try:
                data = screen_resume()

                if isinstance(data, str):
                    st.warning(data)
                else:
                    prompt = f"""
You are HRMATE, an AI recruitment assistant.
Compare the resume with the job description.
List matching skills, missing or unconfirmed skills,
relevant projects, and suggested interview questions.
Use only supplied evidence. Do not invent facts.
This is decision support, not an automatic hiring decision.

RESUME:
{data['resume']}

JOB DESCRIPTION:
{data['job_description']}
"""
                    response = create_llm().invoke(prompt)
                    st.markdown(response.content)

            except Exception as e:
                st.error(f"Screening failed: {e}")

with tab3:
    st.header("Available Interview Slots")

    if st.button("Check Slots"):
        try:
            slots = get_interview_slots()

            if isinstance(slots, str):
                st.info(slots)
            else:
                st.dataframe(slots, use_container_width=True)
        except Exception as e:
            st.error(f"Could not load slots: {e}")
