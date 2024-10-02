import json
import re
import os

polite_words = {'please', 'thank', 'thanks', 'sorry', 'excuse', 'pardon', 'appreciate',
                'grateful', 'kindly', 'would you', 'could you', 'might you', 'if you please', 
                'most obliged', 'be so kind', 'if you would', 'forgive me', 'your humble servant', 
                'I trust', 'your obedient servant', 'may I', 'allow me', 'might I', 'perhaps you could'}

formal_words = {'therefore', 'moreover', 'hence', 'thus', 'notwithstanding', 'consequently',
                'respectfully', 'endeavor', 'commence', 'forthwith', 'inasmuch as', 'heretofore', 
                'inasmuch', 'whereupon', 'thereupon', 'hitherto', 'whom', 'shall', 'must', 'be it known',
                'on behalf of', 'pursuant to', 'in accordance with', 'by virtue of', 'as per'}

lexical_rich_min_length = 5  

def preprocess_text(text):
    text = text.lower()
    text = re.sub(r'[^a-z0-9\s]', '', text)  
    words = text.split()  
    return words

def is_polite(word):
    polite_modal_verbs = {'could', 'might', 'would', 'may', 'should', 'can'}
    return word in polite_words or word in polite_modal_verbs

def is_formal(word):
    return word in formal_words or len(word) > lexical_rich_min_length

def categorize_word(word):
    polite = is_polite(word)
    formal = is_formal(word)
    lexical_rich = len(word) > lexical_rich_min_length
    other = not (polite or formal or lexical_rich)
    return polite, formal, lexical_rich, other

def structure_words_by_category(categorized_words):
    polite_words = [entry['word'] for entry in categorized_words if entry['polite']]
    formal_words = [entry['word'] for entry in categorized_words if entry['formal']]
    lexical_rich_words = [entry['word'] for entry in categorized_words if entry['lexical_rich']]
    other_words = [entry['word'] for entry in categorized_words if not (entry['polite'] or entry['formal'] or entry['lexical_rich'])]
    return polite_words, formal_words, lexical_rich_words, other_words

def categorize_words(words):
    categorized_words = []
    for word in words:
        polite, formal, lexical_rich, other = categorize_word(word)
        categorized_words.append({
            'word': word,
            'polite': polite,
            'formal': formal,
            'lexical_rich': lexical_rich,
            'other': other
        })
    
    return categorized_words

def file_to_json(filename):
    with open(filename, 'r') as f:
        text = f.read()
    words = preprocess_text(text)
    categorized_words = categorize_words(words)
    polite, formal, lexical_rich, other = structure_words_by_category(categorized_words)
    return {
        "polite": polite,
        "formal": formal,
        "lexical_rich": lexical_rich,
        "other": other  
    }

letters_dir = '/Users/sgiannuzzi/Desktop/english145A/letters'
data = {}
for filename in os.listdir(letters_dir):
    if filename.endswith('.txt'):
        letter_path = os.path.join(letters_dir, filename)
        letter_name = os.path.splitext(filename)[0]  
        data[letter_name] = file_to_json(letter_path)

with open('word_categories.json', 'w') as f:
    json.dump(data, f, indent=4)

print("Words categorized and saved to 'word_categories.json'")
