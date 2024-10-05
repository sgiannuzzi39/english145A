import spacy
import numpy as np
from sklearn.manifold import TSNE
import json

nlp = spacy.load("en_core_web_md")

def load_and_preprocess(filepath):
    with open(filepath, 'r') as file:
        text = file.read().lower()
    doc = nlp(text)
    tokens = [token.text for token in doc if token.is_alpha]  
    return tokens

speech_words = load_and_preprocess("/Users/sgiannuzzi/Desktop/english145A/quotes/marianne_total.txt")
letter_words = load_and_preprocess("/Users/sgiannuzzi/Desktop/english145A/letters/marianne_total.txt")

common_topics = ["love", "people", "suffering", "family", "money", "society", "friendship", "marriage", "virtue", "pain"]

all_words = speech_words + letter_words + common_topics

def get_embeddings(words):
    return np.array([nlp(word).vector for word in words if word in nlp.vocab])

word_embeddings = get_embeddings(all_words)

tsne = TSNE(n_components=2, random_state=0)
reduced_embeddings = tsne.fit_transform(word_embeddings)

speech_reduced = reduced_embeddings[:len(speech_words)]
letter_reduced = reduced_embeddings[len(speech_words):len(speech_words) + len(letter_words)]
topic_reduced = reduced_embeddings[len(speech_words) + len(letter_words):]

embedding_data = []

for i, word in enumerate(speech_words):
    embedding_data.append({"word": word, "x": float(speech_reduced[i][0]), "y": float(speech_reduced[i][1]), "source": "speech"})

for i, word in enumerate(letter_words):
    embedding_data.append({"word": word, "x": float(letter_reduced[i][0]), "y": float(letter_reduced[i][1]), "source": "letters"})

for i, word in enumerate(common_topics):
    embedding_data.append({"word": word, "x": float(topic_reduced[i][0]), "y": float(topic_reduced[i][1]), "source": "topic"})

with open("embedding_data_with_topics.json", "w") as f:
    json.dump(embedding_data, f)

print("Word embeddings with common topics saved to 'embedding_data_with_topics.json'")
