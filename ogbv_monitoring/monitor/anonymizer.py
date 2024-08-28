import re
from langdetect import detect
from textblob import TextBlob

def anonymize_tweet(text):
    text = re.sub(r'@\w+', '[USER]', text)
    text = re.sub(r'http\S+|www\S+', '[LINK]', text)
    return text

def detect_language(text):
    try:
        return detect(text)
    except:
        return "unknown"

def analyze_sentiment(text):
    blob = TextBlob(text)
    return blob.sentiment.polarity, blob.sentiment.subjectivity
