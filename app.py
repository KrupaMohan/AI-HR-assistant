import os
# Disable Streamlit's file watcher *before* importing streamlit to avoid issues with certain modules like torch
os.environ["STREAMLIT_WATCHER_TYPE"] = "none"

import types, sys
# Create a stub for 'torch.classes' to avoid Streamlit watcher trying to inspect it
if "torch.classes" not in sys.modules:
    torch_classes_stub = types.ModuleType("torch.classes")
    torch_classes_stub.__path__ = []
    sys.modules["torch.classes"] = torch_classes_stub

import streamlit as st
import torch
print(torch.__version__)

from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Set page configuration - must be the first Streamlit command
st.set_page_config(
    page_title="AI HR Assistant - Smart Resume Screening",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS to remove white spaces
st.markdown("""
    <style>
        .block-container { padding-top: 0; padding-bottom: 0; }
        .main { padding-top: 0; padding-bottom: 0; }
    </style>
""", unsafe_allow_html=True)

# Import modules
from components.sidebar import render_sidebar
from views.home import render_home
from views.upload import render_upload
from views.results import render_results

# Custom styling
with open("assets/style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Initialize session state
if "page" not in st.session_state:
    st.session_state.page = "home"
if "resumes" not in st.session_state:
    st.session_state.resumes = {}
if "job_description" not in st.session_state:
    st.session_state.job_description = ""
if "results" not in st.session_state:
    st.session_state.results = {}
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Render sidebar
render_sidebar()

# Render current page
if st.session_state.page == "home":
    render_home()
elif st.session_state.page == "upload":
    render_upload()
elif st.session_state.page == "results":
    render_results()

def render_home():
    st.write("Rendering HOME page")
    # ...

def render_upload():
    st.write("Rendering UPLOAD page")
    # ...

def render_results():
    st.write("Rendering RESULTS page")
    # ...

def extract_categories(text):
    # ... existing code ...
    for category, pattern in patterns.items():
        # ... existing code ...
        categories[category] = ' '.join(category_text) if category_text else ''
        print(f"{category}: {categories[category]}")  # Add this line for debugging
    return categories
