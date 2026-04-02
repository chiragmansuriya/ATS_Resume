import streamlit as st
import google.generativeai as genai
import os
import PyPDF2 as pdf

# Load API key
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
except:
    from dotenv import load_dotenv
    load_dotenv()
    api_key = os.getenv("GOOGLE_API_KEY")

genai.configure(api_key=api_key)

# Gemini Response
def get_gemini_response(input):
    model = genai.GenerativeModel('gemini-2.0-flash')  # ✅ updated model
    response = model.generate_content(input)
    return response.text

def input_pdf_text(uploaded_file):
    reader = pdf.PdfReader(uploaded_file)
    text = ""
    for page in range(len(reader.pages)):
        page = reader.pages[page]
        text += str(page.extract_text())
    return text

# Prompt Template
input_prompt = """
Hey act like a skilled or very experience ATS (Application Tracking System) with a 
deep understanding of tech field, software engineering, data science, data analyst and 
big data engineer.

Your task is to evaluate the resume based on the given job description.

You must consider the job market is very competitive and you should provide
best assistance for improving the resumes. 
Assign the percentage matching based on JD and the missing keywords 
with high accuracy.

resume: {text}
description: {jd}

Expected Response Structure:
JD match: <percentage_match>%
Missing Keywords: [keyword1, keyword2, ...]
Profile Summary: summary of the profile
"""

# Streamlit app
st.title("Smart ATS")
st.text("Improve Your Resume ATS")
jd = st.text_area("Paste the Job Description")
uploaded_file = st.file_uploader("Upload Your Resume", type="pdf", help="Please upload the resume")

submit = st.button("Submit")

if submit:
    if uploaded_file is not None and jd.strip() != "":
        with st.spinner("Analyzing your resume..."):
            text = input_pdf_text(uploaded_file)
            response = get_gemini_response(input_prompt.format(text=text, jd=jd))  # ✅ fixed
            st.subheader("Analysis Result")
            st.write(response)
    elif uploaded_file is None:
        st.warning("Please upload your resume PDF.")
    else:
        st.warning("Please paste the Job Description.")