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

def get_embeddings(words):
    return np.array([nlp(word).vector for word in words if word in nlp.vocab])

speech_embeddings = get_embeddings(speech_words)
letter_embeddings = get_embeddings(letter_words)

all_embeddings = np.vstack([speech_embeddings, letter_embeddings])

tsne = TSNE(n_components=2, random_state=0)
reduced_embeddings = tsne.fit_transform(all_embeddings)

embedding_data = []

for i, (x, y) in enumerate(reduced_embeddings[:len(speech_embeddings)]):
    embedding_data.append({
        "word": speech_words[i],
        "x": float(x),
        "y": float(y),
        "source": "speech"
    })

for i, (x, y) in enumerate(reduced_embeddings[len(speech_embeddings):]):
    embedding_data.append({
        "word": letter_words[i],
        "x": float(x),
        "y": float(y),
        "source": "letters"
    })

with open("embedding_data.json", "w") as f:
    json.dump(embedding_data, f, indent=4)

print("Embedding data saved to embedding_data.json")
