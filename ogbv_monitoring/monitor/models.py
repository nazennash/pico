from django.db import models
from django.contrib.auth.models import User

class Tweet(models.Model):
    user = models.CharField(max_length=255)
    text = models.TextField()
    language = models.CharField(max_length=20, default="unknown")
    created_at = models.DateTimeField()
    polarity = models.FloatField(default=0.0)
    subjectivity = models.FloatField(default=0.0)

    def __str__(self):
        return f"Tweet by {self.user} in {self.language} on {self.created_at}"

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    institution = models.CharField(max_length=255)
    access_level = models.CharField(max_length=50, choices=[('Researcher', 'Researcher'), ('Policymaker', 'Policymaker')])

    def __str__(self):
        return self.user.username
