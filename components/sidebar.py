import streamlit as st

def render_sidebar():
    with st.sidebar:
        st.markdown(f"<h1 class='header-logo'>AI HR Assistant</h1>", unsafe_allow_html=True)
        st.markdown("### Smart Resume Screening")
        
        st.markdown("---")
        
        # Navigation
        nav_options = {
            "home": "🏠 Home",
            "upload": "📤 Upload & Process",
            "results": "📊 Results"
        }
        
        # Disable results if no results are available
        results_disabled = len(st.session_state.results) == 0
        
        if st.button(nav_options["home"], use_container_width=True):
            st.session_state.page = "home"
            st.rerun()
            
        if st.button(nav_options["upload"], use_container_width=True):
            st.session_state.page = "upload"
            st.rerun()
            
        results_btn = st.button(
            nav_options["results"], 
            use_container_width=True, 
            disabled=results_disabled
        )
        
        if results_btn:
            st.session_state.page = "results"
            st.rerun()
        
        st.markdown("---")
        
        # Status indicators
        st.markdown("### Status")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Resumes**")
        with col2:
            resume_count = len(st.session_state.resumes)
            st.markdown(f"<span style='color: {'var(--success)' if resume_count > 0 else 'var(--error)'}'>{resume_count}</span>", 
                       unsafe_allow_html=True)
            
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Job Description**")
        with col2:
            has_job = bool(st.session_state.job_description)
            st.markdown(f"<span style='color: {'var(--success)' if has_job else 'var(--error)'}'>{('✓' if has_job else '✗')}</span>", 
                       unsafe_allow_html=True)
            
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Results**")
        with col2:
            has_results = len(st.session_state.results) > 0
            st.markdown(f"<span style='color: {'var(--success)' if has_results else 'var(--error)'}'>{('✓' if has_results else '✗')}</span>", 
                       unsafe_allow_html=True)
            
        st.markdown("---")
        
        # Export and Clear options
        export_btn = st.button(
            "📤 Export Results", 
            use_container_width=True,
            disabled=not has_results
        )
        
        if export_btn:
            # Implement export functionality
            pass
        
        if st.button("🗑️ Clear All Data", use_container_width=True):
            st.session_state.resumes = {}
            st.session_state.job_description = ""
            st.session_state.results = {}
            st.toast("All data has been cleared!", icon="🗑️")
            st.rerun()
        
        st.markdown("---")
        
        # App info
        st.markdown("### About")
        st.markdown("""
        AI HR Assistant uses advanced AI and NLP to match resumes to job descriptions.
        
        - Upload multiple resumes (PDF)
        - Enter or select job descriptions
        - Get ranked results instantly
        """)
        
        st.markdown("---")
        st.markdown("© 2025 AI HR Assistant. All rights reserved.")