import facebook
from decouple import config
from .models import Tweet
from .anonymizer import detect_language, anonymize_tweet, analyze_sentiment

def get_facebook_posts():
    graph = facebook.GraphAPI(access_token=config('FACEBOOK_ACCESS_TOKEN'))
    posts = graph.get_connections(id='me', connection_name='posts')

    for post in posts['data']:
        if 'message' in post:
            anonymized_text = anonymize_tweet(post['message'])
            language = detect_language(anonymized_text)
            sentiment_polarity, sentiment_subjectivity = analyze_sentiment(anonymized_text)
            tweet = Tweet(user="FacebookUser", text=anonymized_text, language=language, created_at=post['created_time'], polarity=sentiment_polarity, subjectivity=sentiment_subjectivity)
            tweet.save()
            print(f"Facebook post saved: {tweet}")
