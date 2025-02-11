import re
from langchain_community.document_loaders import PDFPlumberLoader
import json
from sentence_transformers import SentenceTransformer, util
import matplotlib.pyplot as plt
import streamlit as st
import os
import tempfile

def extract_text_pdf(pdf_path):
    loader = PDFPlumberLoader(pdf_path)
    docs = loader.load()
    text = ''
    for doc in docs:
        text += doc.page_content # Append extracted text
    return text 

def extract_name_from_resume(text):
    name = None
    pattern = r"(\b[A-Z][a-z]+\b)\s(\b[A-Z][a-z]+\b)"
    match = re.search(pattern, text)
    if match:
        name = match.group()
    return name

def extract_email_from_resume(text):
    email = None
    pattern = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"
    match = re.search(pattern, text)
    if match:
        email = match.group()
    return email

def extract_skills_from_resume(text, skills_list):
    skills = []
    for skill in skills_list:
        pattern = r"\b{}\b".format(re.escape(skill))
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            skills.append(skill)
    return skills

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

def extracting_experience(text):
    pattern = r"WORK EXPERIENCE\n(.*?)\nEDUCATION"
    match = re.search(pattern, text, re.DOTALL)
    if match:
        return match.group(1).strip()
    return None

def normalize_text(data):
    if isinstance(data, str):
        return data
    elif isinstance(data, list):
        return " ".join(normalize_text(item) for item in data)
    elif isinstance(data, dict):
        return " ".join(normalize_text(value) for value in data.values())
    else:
        return str(data)

def match_resume_to_job(resume_text, job_description, model):
    embeddings = model.encode([resume_text, job_description], convert_to_tensor=True)
    similarity = util.cos_sim(embeddings[0], embeddings[1])
    return similarity.item()

def compute_skill_match(skills, job_description):
    matched_skills = [skill for skill in skills if skill.lower() in job_description.lower()]
    return len(matched_skills) / len(skills) if skills else 0

def rank_candidates(resumes, job_description, model):
    scores = []
    for resume in resumes:
        skills_text = normalize_text(resume.get("Skills", []))
        experience_text = normalize_text(resume.get("Experience", {}))
        education_text = normalize_text(resume.get("Education", {}))

        # Compute similarity scores
        skill_score = match_resume_to_job(skills_text, job_description, model)
        experience_score = match_resume_to_job(experience_text, job_description, model)
        education_score = match_resume_to_job(education_text, job_description, model)
        keyword_match_score = compute_skill_match(resume.get("Skills", []), job_description)

        # Weighted total score
        total_score = 0.5 * skill_score + 0.4 * experience_score + 0.1 * education_score + 0.1 * keyword_match_score

        # Collect scores
        scores.append({
            "Name": resume.get("Name") or resume["Contact Information"]["Name"],
            "Skill Score": skill_score,
            "Experience Score": experience_score,
            "Education Score": education_score,
            "Keyword Match Score": keyword_match_score,
            "Total Score": total_score
        })

    return sorted(scores, key=lambda x: x["Total Score"], reverse=True)

def plot_scores(ranked_candidates):
    names = [candidate['Name'] for candidate in ranked_candidates]
    skill_scores = [candidate['Skill Score'] for candidate in ranked_candidates]
    experience_scores = [candidate['Experience Score'] for candidate in ranked_candidates]
    education_scores = [candidate['Education Score'] for candidate in ranked_candidates]
    keyword_match_scores = [candidate['Keyword Match Score'] for candidate in ranked_candidates]

    # Plot setup
    bar_width = 0.2
    index = range(len(names))

    # Create bars for each category
    plt.bar(index, skill_scores, bar_width, label="Skills")
    plt.bar([i + bar_width for i in index], experience_scores, bar_width, label="Experience")
    plt.bar([i + 2 * bar_width for i in index], education_scores, bar_width, label="Education")
    plt.bar([i + 3 * bar_width for i in index], keyword_match_scores, bar_width, label="Keyword Match")

    # Configure plot details
    plt.xticks([i + 1.5 * bar_width for i in index], names)
    plt.xlabel("Candidates")
    plt.ylabel("Scores")
    plt.title("Candidate Comparison")
    plt.legend()

    # Show plot in Streamlit
    st.pyplot(plt)

def main():
    st.title("Resume Ranker Parser App")

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
        experience = extracting_experience(text)

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

        # Job description for matching
        # job_description = """Looking for a candidate with expertise in Python, Machine Learning, NLP, and SQL. 
        # Must have experience in building predictive models and working with large datasets."""
        # Use st.file_uploader to allow users to upload a file
        # Use st.text_area for multi-line text input
        job_description = st.text_area("Paste your job description here:")

        # Check if the user has entered something
        if job_description:
            st.write("Job Description Entered:")
            st.write(job_description)
        # Rank candidates
        model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')
        ranked_candidates = rank_candidates([{"Name": name, "Skills": skills, "Experience": experience, "Education": education}], job_description, model)

        # Display ranked candidates
        st.subheader("Ranked Candidates")
        for candidate in ranked_candidates:
            st.write(f"**Name:** {candidate['Name']}")
            st.write(f"**Skill Score:** {candidate['Skill Score']:.2f}")
            st.write(f"**Experience Score:** {candidate['Experience Score']:.2f}")
            st.write(f"**Education Score:** {candidate['Education Score']:.2f}")
            st.write(f"**Total Score:** {candidate['Total Score']:.2f}")
            st.write("-" * 30)  # Separator for readability

        # Plot scores
        plot_scores(ranked_candidates)

if __name__ == "__main__":
    main()