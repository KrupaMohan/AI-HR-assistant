import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import re

# Load the sentence transformer model
model = None

def get_model():
    """Load the sentence transformer model lazily to save memory"""
    global model
    if model is None:
        model = SentenceTransformer('all-MiniLM-L6-v2')
    return model

def get_embedding(text):
    """Get embedding vector for a text using sentence transformer"""
    model = get_model()
    return model.encode(text)

def calculate_similarity(text1, text2):
    """Calculate cosine similarity between two texts"""
    # Get embeddings
    embedding1 = get_embedding(text1).reshape(1, -1)
    embedding2 = get_embedding(text2).reshape(1, -1)
    
    # Calculate cosine similarity
    similarity = cosine_similarity(embedding1, embedding2)[0][0]
    
    return similarity

def extract_categories(text):
    """Extract different categories of information from text"""
    # Define regex patterns for different categories
    patterns = {
        'education': r'(?i)(degree|bachelor|master|phd|diploma|certification|university|college|school|education|academic)',
        'experience': r'(?i)(experience|work|job|position|role|career|employment|year|month|project|achievement|accomplishment)',
        'skills': r'(?i)(skill|technology|software|programming|language|tool|framework|proficiency|proficient|knowledge|expertise)',
        'projects': r'(?i)(project|portfolio|github|implementation|developed|built|created|designed|system)',
        'certifications': r'(?i)(certification|certificate|certified|credential|qualification|license)',
    }
    
    # Extract text for each category
    categories = {}
    for category, pattern in patterns.items():
        # Find all matches
        matches = re.finditer(pattern, text)
        
        # Extract sentences containing matches (simplified approach)
        category_text = []
        for match in matches:
            start = max(0, match.start() - 100)
            end = min(len(text), match.end() + 100)
            category_text.append(text[start:end])
        
        # Join all extracted text for this category
        categories[category] = ' '.join(category_text) if category_text else ''
    
    return categories

def compare_resumes_to_job(resumes, processed_job_desc):
    """Compare each resume to the job description and calculate similarity scores.
    Returns a dictionary with resume names as keys and scores as values.
    """
    results = {}
    
    # Get job description embedding for overall similarity
    job_embedding = get_embedding(processed_job_desc).reshape(1, -1)
    
    # Extract categories from job description
    job_categories = extract_categories(processed_job_desc)
    
    # Compare each resume to the job description
    for name, data in resumes.items():
        # Get resume processed text
        resume_text = data["processed_text"]
        raw_resume_text = data["raw_text"]
        
        # Get resume embedding for overall similarity
        resume_embedding = get_embedding(resume_text).reshape(1, -1)
        
        # Calculate overall similarity
        overall_similarity = cosine_similarity(resume_embedding, job_embedding)[0][0]
        
        # Extract categories from resume
        resume_categories = extract_categories(raw_resume_text)
        
        # Calculate category-specific similarities
        category_scores = {}
        for category, job_category_text in job_categories.items():
            if job_category_text and category in resume_categories and resume_categories[category]:
                # Calculate similarity for this category
                category_similarity = calculate_similarity(
                    resume_categories[category],
                    job_category_text
                )
                category_scores[category] = category_similarity
            else:
                # No text for this category in either job or resume
                category_scores[category] = 0.0
        
        # Extract potential keywords (simplified approach)
        keywords = []
        for word in processed_job_desc.split():
            if len(word) > 4 and word in resume_text:  # Simple keyword matching
                keywords.append(word)
        
        # Store result
        results[name] = {
            "score": overall_similarity,
            "category_scores": category_scores,
            "keywords": keywords[:10]  # Limit to top 10 keywords
        }
    
    return results