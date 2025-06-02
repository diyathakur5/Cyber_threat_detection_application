import matplotlib
matplotlib.use('Agg')
import re
import requests
import io
import json
import base64
import random
import joblib
import os
import pandas as pd
import plotly.graph_objs as go
from plotly.offline import plot
from datetime import datetime
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from django.http import HttpResponse
from urllib.parse import urlparse
from datetime import datetime, timedelta
from rest_framework import viewsets
from .models import SpamMessage, SpamURL, SpamPhoneNumber
from .serializers import SpamMessageSerializer, SpamURLSerializer, SpamPhoneNumberSerializer

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
message_model = joblib.load('model/spam_message_model.pkl')
message_vectorizer = joblib.load('model/vectorizer.pkl')
model_path = os.path.join('app', 'models', 'url_model.pkl')
vectorizer_path = os.path.join('app', 'models', 'url_vectorizer.pkl')

try:
    url_model = joblib.load(model_path)
    url_vectorizer = joblib.load(vectorizer_path)
except FileNotFoundError:
    url_model = None
    url_vectorizer = None
    print("URL spam detection model or vectorizer not found!")

def home(request):
    return render(request, 'home.html')  # Your homepage with links

def predict_message(request):
    prediction = None

    if request.method == "POST":
        message = request.POST.get('message', '').strip()

        if message:
            # Check if message is already reported
            if SpamMessage.objects.filter(content=message).exists():
                prediction = "Reported Spam ⚠️"
            else:
                # ML prediction
                vectorized_msg = message_vectorizer.transform([message])
                pred = message_model.predict(vectorized_msg)[0]
                prediction = "Spam " if pred == 1 else "Not Spam ✅"

    return render(request, "predict_message.html", {"message_prediction": prediction})
   
@csrf_exempt


def predict_url(request):
    prediction = None

    if request.method == "POST":
        url = request.POST.get('url', '').strip()

        if url:
            if SpamURL.objects.filter(url=url).exists():
                prediction = "Reported Spam URL "
            elif url_model is None or url_vectorizer is None:
                prediction = "Model not loaded. Please try again later."
            else:
                vectorized_url = url_vectorizer.transform([url])
                pred = url_model.predict(vectorized_url)[0]
                prediction = "Spam " if pred == 1 else "Safe "
        else:
            prediction = "Please enter a URL."

    return render(request, "predict_url.html", {"url_prediction": prediction})

def home(request):
    states = ['Maharashtra', 'Tamil Nadu', 'Karnataka', 'Uttar Pradesh', 'Delhi', 'Gujarat', 'West Bengal']
    crime_rates = [520, 470, 430, 410, 390, 370, 360]

    return render(request, "home.html", {
        "states": states,
        "crime_rates": crime_rates,
    })

def check_number(request):
    if request.method == 'POST':
        number = request.POST.get('phone_number', '').strip()
        
        result = "This number appears to be safe. "  # Default
        
        # Rule-based detection (basic logic)
        if SpamPhoneNumber.objects.filter(phone_number=number).exists():
            result = "Reported Spam Number ⚠️"
        elif (
            number.startswith("140") or 
            number.startswith("700") or
            number.startswith("44") or
            number.startswith("11") or
            number.startswith("+1") or
            number.startswith("91") or
            number.startswith("+44") or
            number.startswith("+234") or
            number.startswith("+63") or
            number.startswith("+62") or
            number.startswith("600") or
            number.startswith("1800") or 
            number.startswith("80085") or
            number in ['1234567890','4444444444', '5555555555', '3333333333', '2222222222', '6666666666',' 7777777777', '8888888888' ,'9999999999', '8888888888', '0000000000']
        ):
            result = " This number is likely spam!"

        return render(request, 'check_number.html', {'number_result': result})
    
    return render(request, 'check_number.html')


def graph(request):
    # Data to be sent to the template
    years = list(range(2018, 2026))
    spam_messages = [120, 180, 250, 400, 560, 710, 820, 950]
    spam_urls = [90, 130, 200, 330, 470, 600, 700, 850]
    spam_numbers = [70, 110, 160, 240, 320, 450, 520, 600]

    chart_data = {
        "years": years,
        "spam_messages": spam_messages,
        "spam_urls": spam_urls,
        "spam_numbers": spam_numbers
    }

    return render(request, 'graph.html', {'chart_data_json': json.dumps(chart_data)})
from django.shortcuts import render


def report_spam(request):
    result = None

    if request.method == 'POST':
        spam_type = request.POST.get('type')
        value = request.POST.get('value').strip()

        if spam_type == 'message':
            if not SpamMessage.objects.filter(content=value).exists():
                SpamMessage.objects.create(content=value)
            result = "Message reported as spam."

        elif spam_type == 'url':
            if not SpamURL.objects.filter(url=value).exists():
                SpamURL.objects.create(url=value)
            result = "URL reported as spam."

        elif spam_type == 'number':
            if not SpamPhoneNumber.objects.filter(phone_number=value).exists():
                SpamPhoneNumber.objects.create(phone_number=value)
            result = "Phone number reported as spam."

    return render(request, 'report_spam.html', {'report_result': result})

class SpamMessageViewSet(viewsets.ModelViewSet):
    queryset = SpamMessage.objects.all()
    serializer_class = SpamMessageSerializer

class SpamURLViewSet(viewsets.ModelViewSet):
    queryset = SpamURL.objects.all()
    serializer_class = SpamURLSerializer

class SpamPhoneNumberViewSet(viewsets.ModelViewSet):
    queryset = SpamPhoneNumber.objects.all()
    serializer_class = SpamPhoneNumberSerializer

    