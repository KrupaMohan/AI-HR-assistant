import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from utils.llm_matching import llm_match_score

def render_results():
    # If no results, redirect to upload page
    if not st.session_state.results:
        st.warning("No results to display. Please process resumes first.")
        st.session_state.page = "upload"
        st.rerun()
    
    st.markdown("<h1 style='text-align:center;'>Results Dashboard</h1>", unsafe_allow_html=True)
    st.markdown("---")
    
    # Resumes Processed metric - left aligned
    st.markdown("<div style='display:flex; justify-content:flex-start; margin-bottom:1rem;'>"
                "<div class='metric-card' style='text-align:left; min-width:200px;'>"
                f"<div class='metric-value' style='font-size:2rem;'>{len(st.session_state.resumes)}</div>"
                "<div class='metric-label' style='font-size:1.1rem;'>Resumes Processed</div>"
                "</div>"
                "</div>", unsafe_allow_html=True)

    # --- RANKING ORDERED LIST (move to top) ---
    st.markdown("### 🏆 Ranking")
    if st.session_state.results:
        sorted_results = sorted(
            st.session_state.results.items(),
            key=lambda x: x[1]["score"],
            reverse=True
        )
        st.markdown("<ol style='font-size:1.2rem;'>", unsafe_allow_html=True)
        for idx, (name, data) in enumerate(sorted_results, 1):
            st.markdown(f"<li><b>Rank {idx}:</b> {name} — <span style='color:#357abd;font-weight:700'>{data['score']*100:.1f}%</span></li>", unsafe_allow_html=True)
        st.markdown("</ol>", unsafe_allow_html=True)

    st.markdown("---")

    # --- CANDIDATE ANALYSIS (middle) ---
    st.markdown("<div style='max-width:600px; width:100%; background:#181c24; border-radius:1rem; padding:2rem 2rem 1rem 2rem; margin:0 auto 2rem auto; box-shadow:0 2px 8px rgba(0,0,0,0.08);'>", unsafe_allow_html=True)
    st.markdown("<h2 style='text-align:center; font-size:2rem; font-weight:700; color:#4a90e2; margin-bottom:0.5rem;'>Candidate Analysis</h2>", unsafe_allow_html=True)
    if st.session_state.results:
        resume_options = list(st.session_state.results.keys())
        selected_resume = st.selectbox(
            "Select Candidate",
            options=resume_options,
            format_func=lambda x: f"#{resume_options.index(x)+1}: {x} ({st.session_state.results[x]['score'] * 100:.1f}%)",
            key="candidate_selectbox"
        )
        if selected_resume:
            st.markdown(f"<div style='text-align:center; font-size:1.2rem;'><b>Selected Candidate:</b> {selected_resume}</div>", unsafe_allow_html=True)
            st.markdown(f"<div style='text-align:center; font-size:1.2rem;'><b>Match Score:</b> <span style='color:#357abd;font-weight:700'>{st.session_state.results[selected_resume]['score'] * 100:.1f}%</span></div>", unsafe_allow_html=True)
            category_scores = st.session_state.results[selected_resume]['category_scores']
            match_score_percent = st.session_state.results[selected_resume]['score'] * 100
            # Define 3 parameters for the Nightingale chart
            parameters = ['skills', 'experience', 'rank']
            values = [
                category_scores.get('skills', 0) * 100,
                category_scores.get('experience', 0) * 100,
                match_score_percent
            ]
            fig = go.Figure()
            fig.add_trace(go.Barpolar(
                r=values,
                theta=parameters,
                marker_color=["#4a90e2", "#50e3c2", "#f5a623"],
                marker_line_color="black",
                marker_line_width=2,
                opacity=0.8
            ))
            fig.update_layout(
                title="Candidate Nightingale Chart",
                polar=dict(
                    radialaxis=dict(
                        visible=True,
                        range=[0, 100]
                    )
                ),
                showlegend=False,
                height=400,
                margin=dict(l=40, r=40, t=40, b=40)
            )
            st.plotly_chart(fig, use_container_width=True)
            if st.session_state.results[selected_resume]['keywords']:
                st.markdown("### 🔑 Key Matched Terms")
                keywords = st.session_state.results[selected_resume]['keywords']
                keyword_html = ""
                for keyword in keywords:
                    keyword_html += f"<span class='keyword-pill'>{keyword}</span>"
                st.markdown(f"<div class='keyword-container'>{keyword_html}</div>", unsafe_allow_html=True)
            st.markdown("### Resume Content")
            with st.expander("View Full Resume Text", expanded=False):
                st.text_area(
                    "Full Text",
                    st.session_state.resumes[selected_resume]["raw_text"],
                    height=300,
                    disabled=True,
                    label_visibility="collapsed"
                )
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("---")

    # --- RANKING BAR CHART (move to bottom) ---
    if st.session_state.results:
        st.markdown("### 📈 Ranking Bar Graph")
        sorted_results = {
            name: data["score"] 
            for name, data in sorted(
                st.session_state.results.items(), 
                key=lambda x: x[1]["score"], 
                reverse=True
            )
        }
        white_bar_color = '#ffffff'  # white
        bar_text_color = '#232837'  # match card/container background
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=list(sorted_results.keys()),
            y=[float(score) * 100 for score in sorted_results.values()],
            marker_color=[white_bar_color for _ in sorted_results.values()],
            text=[f"<span style='color:{bar_text_color}; font-weight:700'>{float(score) * 100:.1f}%</span>" for score in sorted_results.values()],
            textposition='auto',
            hoverinfo='y',
        ))
        fig.update_layout(
            title="Resume Match Scores",
            xaxis_title="Resume",
            yaxis_title="Match Score (%)",
            yaxis=dict(range=[0, 100]),
            height=250,
            margin=dict(l=20, r=20, t=40, b=20),
        )
        fig.update_traces(textfont_size=16)
        st.plotly_chart(fig, use_container_width=True)

def get_color_for_score(score):
    if score >= 0.8:
        return "rgba(56, 176, 0, 0.7)"  # Green (success)
    elif score >= 0.6:
        return "rgba(44, 98, 240, 0.7)"  # Blue (primary)
    elif score >= 0.4:
        return "rgba(255, 190, 11, 0.7)"  # Yellow (warning)
    else:
        return "rgba(230, 57, 70, 0.7)"  # Red (error)

def compare_resumes_to_job(resumes, job_description):
    results = {}
    for name, data in resumes.items():
        score = llm_match_score(job_description, data["raw_text"])
        results[name] = {
            "score": score / 100.0,  # Normalize to 0-1 for consistency
            "category_scores": {},   # You can fill this in later if needed
            "keywords": []           # You can fill this in later if needed
        }
    return results