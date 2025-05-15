import streamlit as st
import pdfplumber
import io
from utils.preprocessing import preprocess_text
from utils.matching import compare_resumes_to_job
import os
import openai

def render_upload():
    if st.session_state.page != "upload":
        return
    st.markdown("<h1>Upload & Process</h1>", unsafe_allow_html=True)
    # Single column layout (no flexbox)
    # Resume upload section
    st.markdown("## 📄 Upload Resumes")

    # Upload area
    uploaded_files = st.file_uploader(
        "Upload PDF resumes",
        type=["pdf"],
        accept_multiple_files=True,
        label_visibility="collapsed"
    )

    if not uploaded_files:
        st.info("Drag and drop PDF resumes here or click to browse")

    # Process uploaded files
    if uploaded_files:
        st.markdown(f"### {len(uploaded_files)} Resumes Uploaded")

        # Process each uploaded file
        for uploaded_file in uploaded_files:
            file_name = uploaded_file.name

            # Check if this resume has already been processed
            if file_name not in st.session_state.resumes:
                try:
                    st.write(f"Processing {file_name}...")
                    pdf_bytes = uploaded_file.getvalue()
                    extracted_text = extract_text_from_pdf(pdf_bytes)
                    processed_text = preprocess_text(extracted_text)
                    st.session_state.resumes[file_name] = {
                        "raw_text": extracted_text,
                        "processed_text": processed_text,
                        "category_scores": {}   # You can fill this in later if needed
                    }
                    st.success(f"✅ {file_name} processed")
                except Exception as e:
                    st.error(f"Error processing {file_name}: {str(e)}")

        # Display processed resumes
        for i, (name, data) in enumerate(st.session_state.resumes.items()):
            with st.expander(f"Resume: {name}"):
                preview_text = data["raw_text"][:500] + "..." if len(data["raw_text"]) > 500 else data["raw_text"]
                st.text_area("Extracted Text Preview", preview_text, height=150)
                if st.button("Remove", key=f"remove_{i}"):
                    del st.session_state.resumes[name]
                    st.rerun()

    # Job description section
    st.markdown("## 📝 Job Description")
    sample_job_content = {
        "software_engineer": "Software Engineer Job Description...",
        "data_scientist": "Data Scientist Job Description...",
        "product_manager": "Product Manager Job Description...",
        "marketing_specialist": "Marketing Specialist Job Description...",
        "custom": "Custom Job Description"
    }

    selected_sample = st.selectbox(
        "Choose a sample job description",
        options=list(sample_job_content.keys())
    )

    if selected_sample == "custom":
        job_description = st.text_area("Enter job description", height=300)
    else:
        job_description = sample_job_content[selected_sample]

    if job_description:
        st.session_state.job_description = job_description

    if st.button("Process Resumes"):
        st.session_state.results = compare_resumes_to_job(st.session_state.resumes, job_description)
        st.session_state.page = "results"
        st.rerun()

def extract_text_from_pdf(pdf_bytes):
    text = ""
    with pdfplumber.open(io.BytesIO(pdf_bytes)) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ""
    return text

def extract_categories(text):
    # Example: Use regex or keyword lists to extract category-specific text
    categories = {
        "skills": ...,
        "experience": ...,
        "education": ...,
        # etc.
    }
    return categories

def score_categories(resume_cats, jd_cats):
    from sentence_transformers import SentenceTransformer, util
    model = SentenceTransformer('all-MiniLM-L6-v2')
    scores = {}
    for cat in resume_cats:
        if resume_cats[cat] and jd_cats[cat]:
            emb_resume = model.encode(resume_cats[cat], convert_to_tensor=True)
            emb_jd = model.encode(jd_cats[cat], convert_to_tensor=True)
            scores[cat] = float(util.pytorch_cos_sim(emb_resume, emb_jd))
        else:
            scores[cat] = 0.0
    return scores

def llm_match_score(job_desc, resume_text):
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return 50.0  # Dummy value

    import openai
    openai.api_key = api_key
   
    prompt = f"Compare the following job description and resume text: Job Description: {job_desc}, Resume Text: {resume_text}"
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",  # or "gpt-4" if you have access
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=10,
        temperature=0
    )
    score_str = response.choices[0].message.content.strip().split()[0]
    return float(score_str)
