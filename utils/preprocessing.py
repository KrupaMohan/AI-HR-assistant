import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

# Download necessary NLTK data
def download_nltk_data():
    required_resources = [
        'punkt',
        'stopwords',
        'wordnet',
        'omw-1.4'
    ]
    for resource in required_resources:
        try:
            nltk.data.find(f'corpora/{resource}' if resource != 'punkt' else f'tokenizers/{resource}')
        except LookupError:
            nltk.download(resource)

# Initialize NLTK resources
download_nltk_data()
stop_words = set(stopwords.words('english'))
lemmatizer = WordNetLemmatizer()

def preprocess_text(text):
    """
    Preprocess text by:
    1. Converting to lowercase
    2. Removing special characters and numbers
    3. Tokenizing
    4. Removing stopwords
    5. Lemmatizing
    """
    text = text.lower()
    text = re.sub(r'[^a-zA-Z\s]', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    
    tokens = word_tokenize(text)
    filtered_tokens = [lemmatizer.lemmatize(token) for token in tokens if token not in stop_words]
    
    return ' '.join(filtered_tokens)
