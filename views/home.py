import streamlit as st

def render_home():
    st.markdown("<h1 style='text-align:center; font-size:2.8rem; font-weight:800; color:#a5d8ff;'>Welcome to AI HR Assistant</h1>", unsafe_allow_html=True)
    st.markdown("""
    <p style='font-size: 1.25rem; margin-bottom: 32px; text-align:center; color:#f8fafc;'>
    Your intelligent solution for automated resume screening and candidate matching
    </p>
    """, unsafe_allow_html=True)

    st.markdown("<h2 style='color:#a5d8ff; font-size:2rem; font-weight:700; margin-bottom:1.5rem;'>🚀 Key Features</h2>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        <h3 style='color:#a5d8ff; font-size:1.3rem; font-weight:700;'>📄 Smart Resume Processing</h3>
        <ul style='font-size:1.1rem; color:#f8fafc;'>
        <li>Upload multiple PDF resumes</li>
        <li>AI-powered text extraction</li>
        <li>Intelligent preprocessing</li>
        </ul>
        <h3 style='color:#a5d8ff; font-size:1.3rem; font-weight:700; margin-top:2rem;'>🔍 Advanced Matching</h3>
        <ul style='font-size:1.1rem; color:#f8fafc;'>
        <li>Deep semantic understanding</li>
        <li>Machine learning algorithms</li>
        <li>Precise candidate ranking</li>
        </ul>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <h3 style='color:#a5d8ff; font-size:1.3rem; font-weight:700;'>📝 Job Analysis</h3>
        <ul style='font-size:1.1rem; color:#f8fafc;'>
        <li>Custom or sample job descriptions</li>
        <li>Skill requirement extraction</li>
        <li>Qualification mapping</li>
        </ul>
        <h3 style='color:#a5d8ff; font-size:1.3rem; font-weight:700; margin-top:2rem;'>💬 AI Assistant</h3>
        <ul style='font-size:1.1rem; color:#f8fafc;'>
        <li>Real-time guidance</li>
        <li>Result interpretation</li>
        <li>Best practices tips</li>
        </ul>
        """, unsafe_allow_html=True)

    st.markdown("<h2 style='text-align:center; color:#a5d8ff; font-size:2rem; font-weight:700; margin-top:2.5rem;'>Ready to streamline your hiring process?</h2>", unsafe_allow_html=True)
    st.markdown("<div style='display:flex; justify-content:center; margin-bottom:1.5rem;'>", unsafe_allow_html=True)
    if st.button("Get Started", key="get_started_btn", help="Start uploading resumes and job descriptions"):
        st.session_state.page = "upload"
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<h2 style='color:#a5d8ff; font-size:2rem; font-weight:700; margin-top:2.5rem;'>How It Works</h2>", unsafe_allow_html=True)
    steps = [
        ("1. Upload", "Upload multiple candidate resumes in PDF format"),
        ("2. Define", "Enter or select a job description to match against"),
        ("3. Process", "Our AI analyzes and matches resumes to the job"),
        ("4. Review", "View ranked results and detailed candidate matches"),
    ]
    cols = st.columns(4)
    for i, (title, desc) in enumerate(steps):
        with cols[i]:
            st.markdown(f"<div style='margin-bottom:0.5rem;'><span style='color:#a5d8ff; font-size:1.5rem; font-weight:700;'>{title}</span></div>", unsafe_allow_html=True)
            st.markdown(f"<div style='color:#f8fafc; font-size:1.05rem;'>{desc}</div>", unsafe_allow_html=True)
    st.markdown("<hr style='margin:2.5rem 0 2rem 0; border:1px solid #232837;'/>", unsafe_allow_html=True)

    st.markdown("<h2 style='color:#a5d8ff; font-size:2rem; font-weight:700; margin-bottom:1.5rem;'>Use Cases</h2>", unsafe_allow_html=True)
    use_cases = [
        ("👩‍💼 HR Professionals", "Automate your hiring process by screening hundreds of resumes in minutes"),
        ("🏢 Hiring Managers", "Quickly identify the most qualified candidates with AI-powered insights"),
        ("🎓 Career Centers", "Help students improve their resumes with AI-driven feedback"),
    ]
    cols = st.columns(3)
    for i, (title, desc) in enumerate(use_cases):
        with cols[i]:
            st.markdown(f"<div style='margin-bottom:0.5rem;'><span style='font-size:1.3rem; font-weight:700; color:#a5d8ff;'>{title}</span></div>", unsafe_allow_html=True)
            st.markdown(f"<div style='color:#f8fafc; font-size:1.05rem;'>{desc}</div>", unsafe_allow_html=True)
