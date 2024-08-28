from django.test import TestCase
from .models import Tweet, UserProfile

class TweetModelTest(TestCase):

    def setUp(self):
        Tweet.objects.create(user="TestUser", text="This is a test tweet", language="en", polarity=0.5, subjectivity=0.5)

    def test_tweet_creation(self):
        tweet = Tweet.objects.get(user="TestUser")
        self.assertEqual(tweet.text, "This is a test tweet")
        self.assertEqual(tweet.language, "en")
        self.assertEqual(tweet.polarity, 0.5)
        self.assertEqual(tweet.subjectivity, 0.5)

class UserProfileModelTest(TestCase):

    def setUp(self):
        user = User.objects.create(username="TestUser")
        UserProfile.objects.create(user=user, institution="Test Institute", access_level="Researcher")

    def test_userprofile_creation(self):
        profile = UserProfile.objects.get(user__username="TestUser")
        self.assertEqual(profile.institution, "Test Institute")
        self.assertEqual(profile.access_level, "Researcher")
