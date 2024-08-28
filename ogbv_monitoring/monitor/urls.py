from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.user_login, name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('transparency/', views.transparency, name='transparency'),
    path('unauthorized/', views.unauthorized, name='unauthorized'),
    path('start-twitter-stream/', views.start_twitter_stream, name='start_twitter_stream'),
    path('start-facebook-stream/', views.start_facebook_stream, name='start_facebook_stream'),
    path('start-instagram-stream/', views.start_instagram_stream, name='start_instagram_stream'),
    path('generate-report/', views.generate_report, name='generate_report'),
    path('logout-confirmation/', views.logout_confirmation, name='logout_confirmation'),
]
