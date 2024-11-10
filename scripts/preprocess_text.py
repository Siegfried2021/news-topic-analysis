import os
import json
import spacy
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from datetime import datetime

# Setup NLP tools
nlp = spacy.load("fr_core_news_md")
stopwords_fr = set(stopwords.words("french"))
lemmatizer = WordNetLemmatizer()

def preprocess_text(text):
    tokens = word_tokenize(text, language='french')
    tokens = [token for token in tokens if token.isalnum() and token.lower() not in stopwords_fr]
    doc = nlp(" ".join(tokens))
    return [token.lemma_ for token in doc]

def preprocess_and_save(input_file, output_file):
    # Load the data from the input file
    with open(input_file, "r", encoding="utf-8") as file:
        data = json.load(file)

    # Process each article and add processed content and title
    processed_data = []
    for article in data:
        processed_data.append({
            "date": article.get("date"),
            "processed_content": preprocess_text(article["content"]),
            "processed_title": preprocess_text(article["title"])
        })

    # Ensure the directory exists and save the processed data
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    with open(output_file, "w", encoding='utf-8') as f:
        json.dump(processed_data, f, ensure_ascii=False, indent=4)

    print(f"Processed data saved to {output_file}")

def run_preprocessing():
    # Get today's date in the format used for filenames
    current_date = datetime.now().strftime('%Y-%m-%d')
    
    # Define input and output files with the current date
    input_file = f"data/articles_RTBF_{current_date}.json"
    output_file = f"data/processed_articles_RTBF_{current_date}.json"
    
    # Process and save data
    preprocess_and_save(input_file, output_file)
