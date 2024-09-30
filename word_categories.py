import json
import re

# Expanded polite and formal word lists (can be further expanded)
polite_words = {
    'please', 'thank', 'thanks', 'sorry', 'excuse', 'pardon', 'appreciate', 'grateful', 
    'kindly', 'would you', 'if you please', 'would be so kind', 'most obliged', 
    'most grateful', 'be so kind', 'if you would', 'pray', 'forgive me', 'your humble servant',
    'would be most kind', 'allow me', 'permit me', 'I beg', 'I beseech', 'may I', 
    'might I', 'your obedient servant', 'I trust', 'with all due respect', 'by your leave',
    'at your convenience', 'I entreat', 'much obliged', 'if it pleases you', 'I remain yours', 
    'with gratitude', 'your kindness', 'much appreciated', 'your servant', 'deferential', 
    'best regards', 'kind regards', 'I most humbly request', 'I apologize', 'would be honored', 
    'honored to', 'I am at your service', 'I request', 'I humbly ask', 'your consideration', 
    'a thousand thanks', 'permit me to thank you', 'I remain your faithful', 'your eternal servant',
    'I trust you will pardon', 'I express my gratitude', 'your most humble'
}

formal_words = {
    'therefore', 'moreover', 'hence', 'thus', 'notwithstanding', 'pursuant', 'consequently', 
    'respectfully', 'endeavor', 'commence', 'herewith', 'hereafter', 'aforementioned', 
    'hereby', 'therein', 'thereafter', 'afore', 'heretofore', 'inasmuch', 'inasmuch as', 
    'whereas', 'forthwith', 'notwithstanding', 'shall', 'henceforth', 'whereupon', 
    'thereupon', 'inasmuch as', 'by virtue of', 'on account of', 'with regard to', 
    'forasmuch as', 'inasmuch as', 'attend', 'be it known', 'it is my duty', 'in compliance with', 
    'it is incumbent upon', 'pursuant to', 'in conformity with', 'hitherto', 'in conclusion', 
    'be advised', 'subsequent to', 'aforementioned', 'hereto', 'be it resolved', 'in the event that', 
    'without delay', 'in due course', 'deem necessary', 'in respect of', 'with respect to'
}

# Lexically rich words could be longer words or predefined, we'll consider words with length > 7 as lexically rich
lexical_rich_min_length = 7

# Function to tokenize text and remove punctuation
def preprocess_text(text):
    # Convert text to lowercase and remove non-alphanumeric characters
    text = text.lower()
    text = re.sub(r'[^a-z0-9\s]', '', text)  # Keep only alphanumeric and space characters
    words = text.split()  # Split by whitespace
    return words

# Function to categorize words
def categorize_words(words):
    polite = [word for word in words if word in polite_words]
    formal = [word for word in words if word in formal_words]
    lexical_rich = [word for word in words if len(word) > lexical_rich_min_length]
    return polite, formal, lexical_rich

# Load the letters
with open('letters/marianne_letter1.txt', 'r') as f1:
    letter1 = f1.read()

with open('letters/marianne_letter2.txt', 'r') as f2:
    letter2 = f2.read()

# Preprocess the text (tokenization and basic cleaning)
letter1_words = preprocess_text(letter1)
letter2_words = preprocess_text(letter2)

# Categorize words for both letters
polite1, formal1, lexical_rich1 = categorize_words(letter1_words)
polite2, formal2, lexical_rich2 = categorize_words(letter2_words)

# Check if the words are being categorized properly
print("Polite words in letter 1:", polite1)
print("Formal words in letter 1:", formal1)
print("Lexically rich words in letter 1:", lexical_rich1)

print("Polite words in letter 2:", polite2)
print("Formal words in letter 2:", formal2)
print("Lexically rich words in letter 2:", lexical_rich2)

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
