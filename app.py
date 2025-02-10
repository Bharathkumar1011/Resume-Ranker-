import streamlit as st
import re
import os
import tempfile
from langchain_community.document_loaders import PDFPlumberLoader

# Function to extract text from PDF
def extract_text_pdf(pdf_path):
    loader = PDFPlumberLoader(pdf_path)
    docs = loader.load()
    text = ''
    for doc in docs:
        text += doc.page_content  # Append extracted text
    return text

# Function to extract name from resume text
def extract_name_from_resume(text):
    name = None
    pattern = r"(\b[A-Z][a-z]+\b)\s(\b[A-Z][a-z]+\b)"
    match = re.search(pattern, text)
    if match:
        name = match.group()
    return name

# Function to extract email from resume text
def extract_email_from_resume(text):
    email = None
    pattern = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"
    match = re.search(pattern, text)
    if match:
        email = match.group()
    return email

# Function to extract skills from resume text
def extract_skills_from_resume(text, skills_list):
    skills = []
    for skill in skills_list:
        pattern = r"\b{}\b".format(re.escape(skill))
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            skills.append(skill)
    return skills

# Function to extract education details from resume text
def extract_education_details(text):
    pattern = r"(?P<university>[\w\s,&]+(?:University|College|Institute|Academy))\n(?P<degree>.+?)\s(?:-\s(?P<gpa>\d\.\d{1,2}\sGPA))?\s(?P<start_date>\w+\s\d{4})\s(?:[-–]\s(?P<end_date>\w+\s\d{4}))?"
    matches = re.finditer(pattern, text)
    education_dict = {
        "University": [],
        "Degree": [],
        "GPA": [],
        "Start Date": [],
        "End Date": [],
    }
    for match in matches:
        education_dict["University"].append(match.group("university").strip())
        education_dict["Degree"].append(match.group("degree").strip())
        education_dict["GPA"].append(match.group("gpa").strip() if match.group("gpa") else "N/A")
        education_dict["Start Date"].append(match.group("start_date").strip())
        education_dict["End Date"].append(match.group("end_date").strip() if match.group("end_date") else "Present")
    return education_dict

# Function to extract experience from resume text
def extract_experience(text):
    pattern = r"WORK EXPERIENCE\n(.*?)\nEDUCATION"
    match = re.search(pattern, text, re.DOTALL)
    if match:
        return match.group(1).strip()
    return None

# Streamlit app
def main():
    st.title("Resume Parser App")

    # Upload PDF resume
    uploaded_file = st.file_uploader("Upload your resume (PDF)", type="pdf")
    if uploaded_file is not None:
        # Save the uploaded file to a temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
            temp_file.write(uploaded_file.read())
            temp_file_path = temp_file.name

        # Extract text from PDF
        text = extract_text_pdf(temp_file_path)

        # Clean up the temporary file
        os.unlink(temp_file_path)


        # Extract details from resume
        name = extract_name_from_resume(text)
        email = extract_email_from_resume(text)
        skills_list = ['Python', 'Data Analysis', 'Machine Learning', 'Communication', 'Project Management', 'Deep Learning', 'SQL', 'Tableau', 'AI', 'Data Visualization', 'Statistical Analysis', 'Big Data', 'Cloud Technologies', 'Problem-Solving', 'Critical Thinking', 'Storytelling']
        skills = extract_skills_from_resume(text, skills_list)
        education = extract_education_details(text)
        experience = extract_experience(text)

        # Display extracted details
        st.subheader("Extracted Resume Details")
        st.write(f"**Name:** {name}")
        st.write(f"**Email:** {email}")
        st.write("**Skills:**")
        st.write(skills)
        st.write("**Education:**")
        st.write(education)
        st.write("**Experience:**")
        st.write(experience)


if __name__ == "__main__":
    main()

    #pip install streamlit langchain_community pdfplumber - run this command in terminal
    #streamlit run app.py - run this command in terminal