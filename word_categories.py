import json
import re

polite_words = {
    'please', 'thank', 'thanks', 'sorry', 'excuse', 'pardon', 'appreciate',
    'grateful', 'kindly', 'would you', 'could you', 'might you', 'if you please', 
    'most obliged', 'be so kind', 'if you would', 'forgive me', 'your humble servant', 
    'I trust', 'your obedient servant', 'may I', 'allow me', 'might I', 'perhaps you could'
}

formal_words = {
    'therefore', 'moreover', 'hence', 'thus', 'notwithstanding', 'consequently',
    'respectfully', 'endeavor', 'commence', 'forthwith', 'inasmuch as', 'heretofore', 
    'inasmuch', 'whereupon', 'thereupon', 'hitherto', 'whom', 'shall', 'must', 'be it known',
    'on behalf of', 'pursuant to', 'in accordance with', 'by virtue of', 'as per'
}

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
    return polite, formal, lexical_rich

def structure_words_by_category(categorized_words):
    polite_words = [entry['word'] for entry in categorized_words if entry['polite']]
    formal_words = [entry['word'] for entry in categorized_words if entry['formal']]
    lexical_rich_words = [entry['word'] for entry in categorized_words if entry['lexical_rich']]
    return polite_words, formal_words, lexical_rich_words

def categorize_words(words):
    categorized_words = []

    for word in words:
        polite, formal, lexical_rich = categorize_word(word)
        categorized_words.append({
            'word': word,
            'polite': polite,
            'formal': formal,
            'lexical_rich': lexical_rich
        })
    
    return categorized_words

with open('letters/willoughby_letter.txt', 'r') as f1:
    letter1 = f1.read()

with open('letters/marianne_letter3.txt', 'r') as f2:
    letter2 = f2.read()

letter1_words = preprocess_text(letter1)
letter2_words = preprocess_text(letter2)

categorized_words1 = categorize_words(letter1_words)
categorized_words2 = categorize_words(letter2_words)

polite1, formal1, lexical_rich1 = structure_words_by_category(categorized_words1)
polite2, formal2, lexical_rich2 = structure_words_by_category(categorized_words2)

data = {
    "letter1": {
        "polite": polite1,
        "formal": formal1,
        "lexical_rich": lexical_rich1
    },
    "letter2": {
        "polite": polite2,
        "formal": formal2,
        "lexical_rich": lexical_rich2
    }
}

with open('word_categories.json', 'w') as f:
    json.dump(data, f, indent=4)

print("Words categorized and saved to 'word_categories.json'")
