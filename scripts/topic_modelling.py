import os
import json
from datetime import datetime
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation
from sklearn.model_selection import GridSearchCV
import numpy as np
import pyLDAvis

def load_processed_articles(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)

def create_dtm(data, max_df=0.5, min_df=2):
    vectorizer = CountVectorizer(max_df=max_df, min_df=min_df)
    return vectorizer.fit_transform(data), vectorizer

def find_best_lda(dtm, topic_range):
    lda = LatentDirichletAllocation(random_state=0)
    param_grid = {'n_components': topic_range, 'learning_decay': [0.5, 0.7, 0.9]}
    grid_search = GridSearchCV(lda, param_grid, cv=3, n_jobs=-1, verbose=2)
    grid_search.fit(dtm)
    return grid_search.best_estimator_

def assign_topics(lda_model, dtm):
    return np.argmax(lda_model.transform(dtm), axis=1).tolist()

def generate_pyldavis(lda_model, dtm, vectorizer, directory="pyLDAvis"):
    # Ensure directory exists
    os.makedirs(directory, exist_ok=True)
    
    # Generate filename with current date
    current_date = datetime.now().strftime('%Y-%m-%d')
    file_path = os.path.join(directory, f"content_topics_vis_{current_date}.html")

    # Create the pyLDAvis visualization
    vocab = vectorizer.get_feature_names_out()
    panel = pyLDAvis.prepare(
        topic_term_dists=lda_model.components_,
        doc_topic_dists=lda_model.transform(dtm),
        doc_lengths=dtm.sum(axis=1).A1,
        vocab=vocab,
        term_frequency=dtm.sum(axis=0).A1
    )
    pyLDAvis.save_html(panel, file_path)
    print(f"Visualization saved as '{file_path}'")

def run_modeling():
    # Get today's date to use for filenames
    current_date = datetime.now().strftime('%Y-%m-%d')
    
    # Define input and output files with the current date
    input_file = f"data/processed_articles_RTBF_{current_date}.json"
    output_file = f"data/processed_articles_RTBF_{current_date}.json"
    
    # Load processed articles for today
    articles = load_processed_articles(input_file)
    content_data = [" ".join(article["processed_content"]) for article in articles]
    
    # Create the document-term matrix (DTM) and vectorizer for content
    content_dtm, content_vectorizer = create_dtm(content_data)
    
    # Find the best LDA model using grid search
    best_lda_content = find_best_lda(content_dtm, topic_range=range(8, 15))
    
    # Assign topics to the articles
    assigned_topics_content = assign_topics(best_lda_content, content_dtm)

    # Add topic numbers to articles and save them back
    for article, topic in zip(articles, assigned_topics_content):
        article["topic_content"] = topic

    # Save updated articles with date-specific output file
    os.makedirs("data", exist_ok=True)
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(articles, f, ensure_ascii=False, indent=4)
    print(f"Processed articles with topics saved to {output_file}")

    # Generate and save a new pyLDAvis visualization with the current date in the filename
    generate_pyldavis(best_lda_content, content_dtm, content_vectorizer)