import json
from sentence_transformers import SentenceTransformer, util

# Load the macro topics and the articles
with open("data/macro_topics.json", "r", encoding="utf-8") as f:
    macro_topics = json.load(f)

with open("data/processed_articles_RTBF.json", "r", encoding="utf-8") as f:
    articles = json.load(f)

# Prepare the macro topics for embedding
topic_names = list(macro_topics.keys())
topic_keywords = [" ".join(macro_topics[topic]) for topic in topic_names]

# Load the pre-trained Sentence-BERT model
model = model = SentenceTransformer('distiluse-base-multilingual-cased-v2')

# Encode macro topics and articles to BERT embeddings
topic_embeddings = model.encode(topic_keywords, convert_to_tensor=True)

# Initialize lists to store the assigned topics
assigned_topics_content = []
assigned_topics_title = []

# Function to find the most similar topic based on cosine similarity
def get_most_similar_topic(text, topic_embeddings, topic_names):
    # Encode the text using BERT
    text_embedding = model.encode(" ".join(text), convert_to_tensor=True)
    # Compute cosine similarity between the article and each topic
    similarities = util.cos_sim(text_embedding, topic_embeddings)
    # Get the index of the most similar topic
    most_similar_index = similarities.argmax()
    # Return the corresponding topic name
    return topic_names[most_similar_index]

# Process each article
for article in articles:
    # Assign the most similar macro topic for content
    assigned_topic_content = get_most_similar_topic(article["processed_content"], topic_embeddings, topic_names)
    assigned_topics_content.append(assigned_topic_content)
    
    # Assign the most similar macro topic for title
    assigned_topic_title = get_most_similar_topic(article["processed_title"], topic_embeddings, topic_names)
    assigned_topics_title.append(assigned_topic_title)

# Save the results
result = {
    "assigned_topics_content": assigned_topics_content,
    "assigned_topics_title": assigned_topics_title
}

with open("data/assigned_topics.json", "w", encoding="utf-8") as f:
    json.dump(result, f, ensure_ascii=False, indent=4)

print("Assigned topics have been saved to 'assigned_topics.json'")