import json
import re
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
import spacy
import gensim
from gensim import corpora
from gensim.models import LdaModel
import nltk
import os

# Load data
with open("data/articles_RTBF.json", "r") as file:
    data = json.load(file)

# Initialize tools
nltk.download('stopwords')
nltk.download('punkt_tab')
nltk.download('wordnet')
stop_words = set(stopwords.words('french'))
lemmatizer = WordNetLemmatizer()

# Load Spacy French model for lemmatization
nlp = spacy.load("fr_core_news_md")

# Preprocess function
def preprocess_text(text):
    # Remove non-alphanumeric characters, except punctuation
    text = re.sub(r'[^a-zA-ZÀ-ÿ0-9.,!?\'\s]', '', text)
    
    # Tokenize
    tokens = word_tokenize(text)
    
    # Remove stopwords and lemmatize
    tokens = [lemmatizer.lemmatize(word.lower()) for word in tokens if word.lower() not in stop_words]
    
    return tokens

# Process both content and title for each article
processed_data = []
for article in data:
    processed_content = preprocess_text(article["content"])
    processed_title = preprocess_text(article["title"])
    processed_data.append({
        "date": article.get("date"),
        "processed_content": processed_content,
        "processed_title": processed_title
    })

