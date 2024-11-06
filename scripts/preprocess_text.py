import json
import re
import os
import spacy
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

# Load data
with open("data/articles_RTBF.json", "r") as file:
    data = json.load(file)

# Initialize tools
nltk.download('stopwords')
nltk.download('punkt_tab')
nltk.download('wordnet')
french_stopwords = set(stopwords.words("french"))
lemmatizer = WordNetLemmatizer()

# Load Spacy French model for lemmatization
nlp = spacy.load("fr_core_news_md")

# Preprocess function
def preprocess_text(text):
    # Tokenize the text with nltk
    tokens = word_tokenize(text, language='french')
    
    # Filter out punctuation and stop words
    tokens = [token for token in tokens if token.isalnum() and token.lower() not in french_stopwords]
    
    # Lemmatize using spacy
    doc = nlp(" ".join(tokens))
    lemmatized_tokens = [token.lemma_ for token in doc]
    
    return lemmatized_tokens

def preprocess_and_save(data, output_filename):
    processed_data = []
    
    for article in data:
        # Process the title and content using a custom preprocess_text function
        processed_content = preprocess_text(article["content"])
        processed_title = preprocess_text(article["title"])
        
        # Append the processed article to the list
        processed_data.append({
            "date": article.get("date"),
            "processed_content": processed_content,
            "processed_title": processed_title
        })
    
    os.makedirs(os.path.dirname(output_filename), exist_ok=True)

    # Save processed data to a JSON file
    with open(output_filename, "w", encoding='utf-8') as outfile:
        json.dump(processed_data, outfile, ensure_ascii=False, indent=4)

preprocess_and_save(data, "data/processed_articles_RTBF.json")
