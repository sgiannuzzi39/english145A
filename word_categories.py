import json
import re

# Expanded polite and formal word lists (can be further expanded)
polite_words = {
    'please', 'thank', 'thanks', 'sorry', 'excuse', 'pardon', 'appreciate', 
    'grateful', 'kindly', 'would you', 'if you please', 'most obliged', 
    'most grateful', 'be so kind', 'if you would', 'pray', 'forgive me', 
    'your humble servant', 'I trust', 'your obedient servant', 'much obliged'
}

formal_words = {
    'therefore', 'moreover', 'hence', 'thus', 'notwithstanding', 'pursuant', 
    'consequently', 'respectfully', 'endeavor', 'commence', 'forthwith', 
    'inasmuch as', 'heretofore', 'inasmuch', 'whereupon', 'thereupon', 
    'be it known', 'it is incumbent upon', 'hitherto', 'forthwith'
}

# Lexically rich words could be longer words or predefined, we'll consider words with length > 7 as lexically rich
lexical_rich_min_length = 7

# Function to tokenize text and remove punctuation
def preprocess_text(text):
    text = text.lower()
    text = re.sub(r'[^a-z0-9\s]', '', text)  # Keep only alphanumeric and space characters
    words = text.split()  # Split by whitespace
    return words

# Function to categorize words
def categorize_words(words, text):
    polite = [word for word in words if word in polite_words]
    formal = [word for word in words if word in formal_words]
    lexical_rich = [word for word in words if len(word) > lexical_rich_min_length]
    
    return polite, formal, lexical_rich

# Load the letters
with open('letters/willoughby_letter.txt', 'r') as f1:
    letter1 = f1.read()

with open('letters/marianne_letter3.txt', 'r') as f2:
    letter2 = f2.read()

# Preprocess the text
letter1_words = preprocess_text(letter1)
letter2_words = preprocess_text(letter2)

# Categorize words and structures
polite1, formal1, lexical_rich1 = categorize_words(letter1_words, letter1)
polite2, formal2, lexical_rich2 = categorize_words(letter2_words, letter2)

# Create data for visualization
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

# Save the data as a JSON file
with open('word_categories.json', 'w') as f:
    json.dump(data, f)

print("Word categories saved to 'word_categories.json'")
