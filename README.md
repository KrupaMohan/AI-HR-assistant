# AI-HR-assistant
# Resume Matcher

A Streamlit-based web application that matches resumes to job descriptions using semantic similarity and category-based scoring.

## Overview

This project helps recruiters and job seekers by:
- Uploading multiple resumes and a job description
- Analyzing and comparing resumes against the job description
- Providing detailed matching scores, category breakdowns, and keyword matches

## Features

- **Resume Upload**: Upload multiple resumes in PDF format
- **Job Description Input**: Paste or upload a job description
- **Semantic Matching**: Uses sentence transformers to compute semantic similarity
- **Category-Based Analysis**: Breaks down matches by education, experience, skills, projects, and certifications
- **Keyword Matching**: Identifies key terms from the job description present in resumes
- **Interactive Results**: View detailed matching scores and analysis in an interactive dashboard

// ... existing code ...
3. Upload resumes and a job description, then view the matching results

## Live Demo

The application is deployed on Streamlit Cloud and can be accessed at:
[AI HR Assistant](https://resume-matcher.streamlit.app)

You can try out the application directly in your browser without any local setup!

## Setup

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/resume-matcher.git
   cd resume-matcher
   ```

2. Create a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows, use: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Start the Streamlit app:
   ```bash
   streamlit run app.py
   ```

2. Open your browser and navigate to the URL shown in the terminal (usually http://localhost:8501)

3. Upload resumes and a job description, then view the matching results

## Project Structure

- `app.py`: Main Streamlit application
- `views/`: UI components for upload, results, and home pages
- `utils/`: Utility functions for resume processing and matching
- `requirements.txt`: List of Python dependencies

## Dependencies

- streamlit
- pandas
- numpy
- scikit-learn
- sentence-transformers
- pdfplumber

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
