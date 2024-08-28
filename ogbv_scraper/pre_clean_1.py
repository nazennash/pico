import re
import json
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

import nltk
try:
    nltk.data.find('corpora/stopwords')
except:
    nltk.download('stopwords')

def clean_text(text):
    text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
    text = re.sub(r'[^A-Za-z\s]', '', text)
    text = text.lower()
    tokens = word_tokenize(text)
    stop_words = set(stopwords.words('english'))
    tokens = [word for word in tokens if word not in stop_words]
    return ' '.join(tokens)

try:
    with open('data.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
except FileNotFoundError:
    print("Error: 'data.json' file not found.")
    exit(1)
except json.JSONDecodeError:
    print("Error: Failed to decode JSON.")
    exit(1)

paragraphs = data.get("paragraphs", [])

cleaned_paragraphs = [clean_text(paragraph) for paragraph in paragraphs]

try:
    with open('pre_cleaned_1.json', 'w', encoding='utf-8') as file:
        json.dump(cleaned_paragraphs, file, indent=4)
    print('Successfully cleaned and saved paragraphs to pre_cleaned_1.json')
except IOError as e:
    print(f'Error saving cleaned data to pre_cleaned_1.json: {e}')
