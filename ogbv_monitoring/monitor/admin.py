from django.contrib import admin
from .models import Tweet, UserProfile

# Register your models here.
admin.site.register(Tweet)
admin.site.register(UserProfile)
