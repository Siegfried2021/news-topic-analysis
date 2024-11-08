# import json
# from sklearn.feature_extraction.text import CountVectorizer
# from sklearn.decomposition import LatentDirichletAllocation
# from sklearn.model_selection import GridSearchCV
# import numpy as np

# # Load the articles
# with open("data/processed_articles_RTBF.json", "r", encoding="utf-8") as f:
#     articles = json.load(f)

# # Prepare data for LDA
# content_data = [" ".join(article["processed_content"]) for article in articles]
# title_data = [" ".join(article["processed_title"]) for article in articles]

# # Initialize CountVectorizer for bag-of-words
# vectorizer = CountVectorizer(max_df=0.95, min_df=2)  # Adjust stop words as needed

# # Transform data into a document-term matrix for content and title
# content_dtm = vectorizer.fit_transform(content_data)
# title_dtm = vectorizer.fit_transform(title_data)

# # Define a range for the number of topics
# topic_range = list(range(10, 16))

# # Function to perform grid search and select the best LDA model
# def find_best_lda(dtm, topic_range):
#     # Define the LDA model and grid search parameters
#     lda = LatentDirichletAllocation(random_state=0)
#     param_grid = {'n_components': topic_range, 'learning_decay': [0.5, 0.7, 0.9]}
#     grid_search = GridSearchCV(lda, param_grid, cv=3, n_jobs=-1, verbose=2)
#     grid_search.fit(dtm)

#     # Get the best model based on grid search results
#     best_lda_model = grid_search.best_estimator_
#     best_num_topics = best_lda_model.n_components
#     return best_lda_model, best_num_topics

# # Find the best model for content and title
# print("Finding best LDA model for content...")
# best_lda_content, best_num_topics_content = find_best_lda(content_dtm, topic_range)

# print("Finding best LDA model for title...")
# best_lda_title, best_num_topics_title = find_best_lda(title_dtm, topic_range)

# # Function to assign topics to articles
# def assign_topics(lda_model, dtm):
#     # Get the topic distribution for each document
#     topic_distributions = lda_model.transform(dtm)
#     # Assign each document the topic with the highest probability
#     assigned_topics = np.argmax(topic_distributions, axis=1)
#     return assigned_topics.tolist()

# # Assign topics to each article's content and title using the best LDA models
# assigned_topics_content = assign_topics(best_lda_content, content_dtm)
# assigned_topics_title = assign_topics(best_lda_title, title_dtm)

# # Save results
# result = {
#     "best_num_topics_content": best_num_topics_content,
#     "assigned_topics_content": assigned_topics_content,
#     "best_num_topics_title": best_num_topics_title,
#     "assigned_topics_title": assigned_topics_title
# }

# with open("data/assigned_topics.json", "w", encoding="utf-8") as f:
#     json.dump(result, f, ensure_ascii=False, indent=4)

# print("Assigned topics have been saved to 'assigned_topics.json'")

import json
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation
from sklearn.model_selection import GridSearchCV
import numpy as np
import pyLDAvis

# Load the articles
with open("data/processed_articles_RTBF.json", "r", encoding="utf-8") as f:
    articles = json.load(f)

# Prepare data for LDA
content_data = [" ".join(article["processed_content"]) for article in articles]
title_data = [" ".join(article["processed_title"]) for article in articles]

# Initialize separate CountVectorizers for content and title
content_vectorizer = CountVectorizer(max_df=0.95, min_df=2)
title_vectorizer = CountVectorizer(max_df=0.95, min_df=2)

# Transform data into a document-term matrix for content and title
content_dtm = content_vectorizer.fit_transform(content_data)
title_dtm = title_vectorizer.fit_transform(title_data)

# Define a range for the number of topics
topic_range = list(range(10, 16))

# Function to perform grid search and select the best LDA model
def find_best_lda(dtm, topic_range):
    lda = LatentDirichletAllocation(random_state=0)
    param_grid = {'n_components': topic_range, 'learning_decay': [0.5, 0.7, 0.9]}
    grid_search = GridSearchCV(lda, param_grid, cv=3, n_jobs=-1, verbose=2)
    grid_search.fit(dtm)
    best_lda_model = grid_search.best_estimator_
    best_num_topics = best_lda_model.n_components
    return best_lda_model, best_num_topics

# Find the best model for content and title
print("Finding best LDA model for content...")
best_lda_content, best_num_topics_content = find_best_lda(content_dtm, topic_range)

print("Finding best LDA model for title...")
best_lda_title, best_num_topics_title = find_best_lda(title_dtm, topic_range)

# Function to assign topics to articles
def assign_topics(lda_model, dtm):
    topic_distributions = lda_model.transform(dtm)
    assigned_topics = np.argmax(topic_distributions, axis=1)
    return assigned_topics.tolist()

# Assign topics to each article's content and title using the best LDA models
assigned_topics_content = assign_topics(best_lda_content, content_dtm)
assigned_topics_title = assign_topics(best_lda_title, title_dtm)

# Save results
result = {
    "best_num_topics_content": best_num_topics_content,
    "assigned_topics_content": assigned_topics_content,
    "best_num_topics_title": best_num_topics_title,
    "assigned_topics_title": assigned_topics_title
}

with open("data/assigned_topics.json", "w", encoding="utf-8") as f:
    json.dump(result, f, ensure_ascii=False, indent=4)

print("Assigned topics have been saved to 'assigned_topics.json'")

# Prepare and save the pyLDAvis visualization for content topics
print("Generating pyLDAvis visualization for content topics...")
vocab_content = content_vectorizer.get_feature_names_out()
term_frequency_content = content_dtm.sum(axis=0).A1

content_panel = pyLDAvis.prepare(
    topic_term_dists=best_lda_content.components_,
    doc_topic_dists=best_lda_content.transform(content_dtm),
    doc_lengths=content_dtm.sum(axis=1).A1,
    vocab=vocab_content,
    term_frequency=term_frequency_content
)
pyLDAvis.save_html(content_panel, 'content_topics_vis.html')
print("Content topic visualization saved as 'content_topics_vis.html'.")

# Repeat for title topics
print("Generating pyLDAvis visualization for title topics...")
vocab_title = title_vectorizer.get_feature_names_out()
term_frequency_title = title_dtm.sum(axis=0).A1

title_panel = pyLDAvis.prepare(
    topic_term_dists=best_lda_title.components_,
    doc_topic_dists=best_lda_title.transform(title_dtm),
    doc_lengths=title_dtm.sum(axis=1).A1,
    vocab=vocab_title,
    term_frequency=term_frequency_title
)
pyLDAvis.save_html(title_panel, 'title_topics_vis.html')
print("Title topic visualization saved as 'title_topics_vis.html'.")
