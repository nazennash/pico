import tweepy
from decouple import config
from .models import Tweet
from .anonymizer import detect_language, anonymize_tweet, analyze_sentiment

auth = tweepy.OAuth1UserHandler(
    config('TWITTER_API_KEY'),
    config('TWITTER_API_SECRET_KEY'),
    config('TWITTER_ACCESS_TOKEN'),
    config('TWITTER_ACCESS_TOKEN_SECRET')
)

bearer_token = config('TWITTER_BEARER_TOKEN')


api = tweepy.API(auth, wait_on_rate_limit=True)

class OGBVStreamClient(tweepy.StreamingClient):
    def on_tweet(self, tweet):
        anonymized_text = anonymize_tweet(tweet.text)
        language = detect_language(anonymized_text)
        sentiment_polarity, sentiment_subjectivity = analyze_sentiment(anonymized_text)
        new_tweet = Tweet(user=tweet.author_id, text=anonymized_text, language=language, created_at=tweet.created_at, polarity=sentiment_polarity, subjectivity=sentiment_subjectivity)
        new_tweet.save()
        print(f"Tweet saved: {new_tweet}")

    def on_error(self, status_code):
        if status_code == 420:
            return False 

def start_stream():
    stream_client = OGBVStreamClient(bearer_token=bearer_token)
    stream_client.add_rules(tweepy.StreamRule(value="gender-based violence OR GBV OR OGBV OR abuse OR violence"))
    stream_client.filter()