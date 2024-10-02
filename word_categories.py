import json
import re
import os
import spacy

nlp = spacy.load("en_core_web_sm")

lexical_rich_min_length = 6

def preprocess_text(text):
    text = text.lower()
    text = re.sub(r'[^a-z\s]', '', text) 
    words = text.split() 
    return words

def classify_politeness(text):
    doc = nlp(text)
    polite_score = 0

    polite_phrases = {
        "please": 2, "could you": 2, "would you mind": 3, "thank you": 2,
        "i apologize": 2, "sorry": 2, "i would appreciate": 3, "might you": 2,
        "if it’s not too much": 3, "excuse me": 2
    }

    for phrase, weight in polite_phrases.items():
        if phrase in text:
            polite_score += weight

    for token in doc:
        if token.lemma_ in {"would", "could", "might", "may", "should"}:
            polite_score += 1  

    for token in doc:
        if token.lemma_ in {"think", "believe", "feel", "hope", "apologize", "sorry"}:
            polite_score += 1

    for sent in doc.sents:
        if any(token.lemma_ in {"could", "would"} for token in sent) and "you" in sent.text:
            polite_score += 2 

    return polite_score

def classify_formality(text):
    doc = nlp(text)
    formal_score = 0
    for token in doc:
        if token.lemma_ in {"therefore", "moreover", "hence", "thus", "inasmuch", "notwithstanding"}:
            formal_score += 2
        if len(token.text) > 7: 
            formal_score += 1

    if len(list(doc.sents)) > 1:  
        formal_score += len(list(doc.sents)) - 1

    return formal_score

def tag_adjectives_adverbs(text):
    doc = nlp(text)
    adjectives_adverbs_count = sum(1 for token in doc if token.pos_ in {"ADJ", "ADV"})
    return adjectives_adverbs_count

def categorize_words(text):
    total_words = len(preprocess_text(text)) 
    categorized_words = {
        'polite': classify_politeness(text),  
        'formal': classify_formality(text),  
        'lexical_rich': sum(1 for word in preprocess_text(text) if len(word) >= lexical_rich_min_length),
        'adjectives_adverbs': tag_adjectives_adverbs(text),
        'total_words': total_words
    }

    return categorized_words

def format_filename(folder, filename):
    base_name = os.path.splitext(filename)[0]  
    base_name = re.sub(r'vol', '', base_name, flags=re.IGNORECASE)  
    base_name = base_name.replace('_', ' ') 
    base_name = re.sub(r'^quotes:?|^letters:?', '', base_name, flags=re.IGNORECASE).strip()  

    if folder == 'quotes':
        if 'total' in base_name:
            if 'marianne' in base_name:
                return "Marianne's Speech, All Volumes"
            elif 'willoughby' in base_name:
                return "Willoughby's Speech, All Volumes"
            elif 'lucy' in base_name:
                return "Lucy's Speech, All Volumes"
            else:
                return base_name
        parts = base_name.split()
        character = parts[0].capitalize()
        volume = re.findall(r'\d+', base_name)[-1] 
        return f"{character} Quotes, Volume {volume}"

    elif folder == 'letters':
        if 'total' in base_name:
            return f"{base_name.split()[0].capitalize()}'s Total Letters"
        parts = base_name.split()
        character = parts[0].capitalize()
        number_word = 'First' if '1' in parts[-1] else 'Second' if '2' in parts[-1] else 'Third'
        return f"{character}'s {number_word} Letter"

def process_folder(folder_path, folder_type):
    folder_data = {}
    
    for filename in os.listdir(folder_path):
        if filename.endswith('.txt'):
            with open(os.path.join(folder_path, filename), 'r') as f:
                text = f.read()
                categorized_data = categorize_words(text)
                formatted_name = format_filename(folder_type, filename)
                folder_data[formatted_name] = categorized_data
    
    return folder_data

quotes_folder = '/Users/sgiannuzzi/Desktop/english145A/quotes'
letters_folder = '/Users/sgiannuzzi/Desktop/english145A/letters'

data = {
    'quotes': process_folder(quotes_folder, 'quotes'),
    'letters': process_folder(letters_folder, 'letters')
}

with open('word_categories.json', 'w') as f:
    json.dump(data, f, indent=4)

print("Words categorized and saved to 'word_categories.json'")
