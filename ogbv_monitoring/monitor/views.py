from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Count, Avg
from .models import Tweet, UserProfile
from .twitter_client import start_stream
from .facebook_client import get_facebook_posts
from .instagram_client import get_instagram_posts
from .anonymizer import detect_language, anonymize_tweet, analyze_sentiment
from django.template.loader import render_to_string
from django.http import HttpResponse
from xhtml2pdf import pisa
import io

def home(request):
    return render(request, 'monitor/home.html')

from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def logout_confirmation(request):
    return render(request, 'monitor/logout_confirmation.html')


def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            return render(request, 'monitor/login.html', {'error': 'Invalid credentials'})
    return render(request, 'monitor/login.html')

def researcher_check(user):
    return user.groups.filter(name='Researchers').exists()

@login_required
@user_passes_test(researcher_check, login_url='unauthorized')
def dashboard(request):
    tweets = Tweet.objects.all().order_by('-created_at')[:10]
    tweet_count = Tweet.objects.count()

    sentiment_trends = Tweet.objects.annotate(date=TruncDay('created_at')).values('date').annotate(polarity_avg=Avg('polarity')).order_by('date')
    sentiment_dates = [trend['date'].strftime('%Y-%m-%d') for trend in sentiment_trends]
    sentiment_values = [trend['polarity_avg'] for trend in sentiment_trends]

    context = {
        'tweets': tweets,
        'tweet_count': tweet_count,
        'sentiment_dates': sentiment_dates,
        'sentiment_values': sentiment_values,
    }
    return render(request, 'monitor/dashboard.html', context)

def transparency(request):
    return render(request, 'monitor/transparency.html')

def unauthorized(request):
    return render(request, 'monitor/unauthorized.html', status=403)

def start_twitter_stream(request):
    start_stream()
    return HttpResponse("Twitter stream started.")

def start_facebook_stream(request):
    get_facebook_posts()
    return HttpResponse("Facebook data collection started.")

def start_instagram_stream(request):
    get_instagram_posts()
    return HttpResponse("Instagram data collection started.")

def generate_report(request):
    tweets = Tweet.objects.all()
    context = {'tweets': tweets}

    html_string = render_to_string('monitor/report.html', context)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="ogbv_report.pdf"'

    result = io.BytesIO()
    pdf = pisa.pisaDocument(io.BytesIO(html_string.encode('UTF-8')), result)

    if not pdf.err:
        response.write(result.getvalue())
        return response
    else:
        return HttpResponse("Error generating PDF", status=500)
