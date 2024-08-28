import requests
from decouple import config
from .models import Tweet
from .anonymizer import detect_language, anonymize_tweet, analyze_sentiment

def get_instagram_posts():
    access_token = config('INSTAGRAM_ACCESS_TOKEN')
    user_id = 'your-instagram-user-id'
    url = f"https://graph.instagram.com/{user_id}/media?fields=id,caption,timestamp&access_token={access_token}"
    response = requests.get(url)

    if response.status_code == 200:
        posts = response.json()['data']
        for post in posts:
            if 'caption' in post:
                anonymized_text = anonymize_tweet(post['caption'])
                language = detect_language(anonymized_text)
                sentiment_polarity, sentiment_subjectivity = analyze_sentiment(anonymized_text)
                tweet = Tweet(user="InstagramUser", text=anonymized_text, language=language, created_at=post['timestamp'], polarity=sentiment_polarity, subjectivity=sentiment_subjectivity)
                tweet.save()
                print(f"Instagram post saved: {tweet}")
