import time
from django.http import JsonResponse
from django.shortcuts import render,redirect
from google_auth_oauthlib.flow import Flow
import os
from Buggy.settings import BASE_DIR,google_scopes
import datetime
from django.contrib.auth.models import User
from Home.models import Profile,Reminder
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
from Home.reminder_handler import start
from datetime import date
from Buggy.whatsapp_connecter import send_message
from .healthchecker import start_checker
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login
start()
start_checker()
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'  # For local dev HTTP

CLIENT_SECRETS_FILE =os.path.join(BASE_DIR,"Home","client_secret.json") 
REDIRECT_URI = 'http://localhost:8000/oauth2callback'
def login_page(request):
    flow = Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE,
        scopes=google_scopes,
        redirect_uri=REDIRECT_URI
    )
    auth_url, _ = flow.authorization_url(
        access_type='offline',
        include_granted_scopes='false',
        prompt='consent'
    )
    return redirect(auth_url)
def logout(request):
    request.session.flush()
    return redirect('/')
def oauth2callback(request):
    flow = Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE,
        scopes=google_scopes,
        redirect_uri=REDIRECT_URI
    )
    flow.fetch_token(authorization_response=request.build_absolute_uri())

    credentials = flow.credentials

    request.session['token'] = credentials.token
    request.session['refresh_token'] = credentials.refresh_token
    request.session['token_uri'] = credentials.token_uri
    request.session['client_id'] = credentials.client_id
    request.session['client_secret'] = credentials.client_secret
    request.session['scopes'] = credentials.scopes
    people_service = build('people', 'v1', credentials=credentials)
    profile = people_service.people().get(
        resourceName='people/me',
        personFields='names,emailAddresses,phoneNumbers,birthdays'
    ).execute()
    name = profile.get('names', [{}])[0].get('displayName', 'No Name')
    email = profile.get('emailAddresses', [{}])[0].get('value', 'No Email')
    phone = profile.get('phoneNumbers', [{}])[0].get('value', 'No Phone')
    birthdays = profile.get('birthdays', [])
    age=21
    if birthdays:
        for b in birthdays:
            date_info = b.get('date', {})
            if 'year' in date_info: 
                birth_year = date_info['year']
                birth_month = date_info['month']
                birth_day = date_info['day']
                today = date.today()
                age = today.year - birth_year
                if (today.month, today.day) < (birth_month, birth_day):age -= 1
                break
       
 
    try:
        user= User.objects.get(email=email)
        login(request,user)
    except User.DoesNotExist:
        if(phone=="No Phone"):phone=919363255562
        else:phone=f"91{phone}"
        newuser=User.objects.create(email=email,username=name)
        profile=Profile.objects.create(user=newuser, phone_number=phone,token=credentials.token,refresh_token=credentials.refresh_token,token_uri= credentials.token_uri,client_id=credentials.client_id,client_secret=credentials.client_secret,age=age)
     
        login(request,newuser)
        send_message({"to":phone,"userdata":{"prompt":0,"name":name,"age":age,"phone":phone}})
    return redirect('home')

@csrf_exempt
def get_data(request):
    if request.method == 'POST':
        try:
            user=request.user
            if(not user.is_anonymous):
                return JsonResponse({'login':True, 'heart_rate':user.profile.heart_rate,'step_count':user.profile.step_count,'calories':user.profile.calories})
        except Exception as e:
            print(e)
            pass
        return JsonResponse({'login':False})
    return render(request,"index.html")



