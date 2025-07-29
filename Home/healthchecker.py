from Buggy.whatsapp_connecter import send_message
from django.contrib.auth import get_user_model
from apscheduler.schedulers.background import BackgroundScheduler
from concurrent.futures import ThreadPoolExecutor
from googleapiclient.discovery import build
from Buggy.settings import BASE_DIR,google_scopes
from google.oauth2.credentials import Credentials
import datetime
import time
from apscheduler.jobstores.memory import MemoryJobStore
from datetime import datetime, timedelta
import traceback
import sys
def fetch_google_data_for_user(user):
    try:
        creds =   creds = Credentials(token=user.profile.token,refresh_token=user.profile.refresh_token,token_uri=user.profile.token_uri,client_id=user.profile.client_id,client_secret=user.profile.client_secret,scopes=google_scopes)
        service = build('people', 'v1', credentials=creds)
        last_synced_at=user.profile.last_synced_at
        latest_end_time = last_synced_at
        start_time_ns =  last_synced_at
        end_time_ns = int(time.time() * 1e9)
        dataset = f"{start_time_ns}-{end_time_ns}"
        service = build('fitness', 'v1', credentials=creds)
        datasources = {}
        totals = {'steps': 0, 'heart_rate': 0, 'distance': False,'calories':0}
        datasources_list = service.users().dataSources().list(userId='me').execute()
        app_names = {
  
  "com.sec.android.app.shealth": "Samsung Health",
  "com.boAt.wristgear": "boAt Wearable",
  "com.samsung.android.app.watchmanager": "Samsung Galaxy Wearable",
  "com.noise.smartwearable": "NoiseFit (Noise Wearable)",
  "com.fastrack.reflex": "Fastrack Reflex",
  "com.huawei.health": "Huawei Health",
  "com.fitbit.FitbitMobile": "Fitbit",
  "com.garmin.android.apps.connectmobile": "Garmin Connect"

}

        for datasource in datasources_list.get('dataSource', []):
            if 'application' in datasource:
                app = datasource['application']
                package_name = app.get('packageName')
                if package_name in app_names:
                    readable_app_name = app_names[package_name]
                    print(f"Detected smartwatch app for user {user.username}: {readable_app_name}")
                    datasources[datasource['dataStreamName']] = datasource['dataStreamId']

        for source_key in datasources:
            result = service.users().dataSources().datasets().get(
                userId='me',
                dataSourceId=datasources[source_key],
                datasetId=dataset
            ).execute()
            for point in result.get('point', []):
                 point_end_time = int(point['endTimeNanos'])
                 if point_end_time <= last_synced_at:continue
                 for field in point['value']:
                    datatype=point['dataTypeName']
                    if(datatype=='com.google.heart_rate.bpm'):
                        totals['heart_rate']=field['fpVal']
                    
                    elif(datatype=="com.google.step_count.delta"):
                        totals['steps']+=field['intVal']
                    elif (datatype=="com.google.calories.expended"):
                        totals["calories"]+=field['fpVal']
                 if point_end_time > latest_end_time:
                    latest_end_time = point_end_time
        if totals['heart_rate']!=0:
            send_message({"to":user.profile.phone_number,"userdata":{"name":user.username,"age":user.profile.age,"language":user.profile.language,"bpm":totals['heart_rate'],"prompt":1}})
            user.profile.heart_rate=totals['heart_rate']
        if totals['steps']!=0:
            user.profile.step_count=totals['steps']
            if totals['steps'] % 100 == 0:
                send_message({"to":user.profile.phone_number,"userdata":{"name":user.username,"age":user.profile.age,"language":user.profile.language,"steps":totals['steps'],"prompt":2}})
        if totals['calories']!=0:
              user.profile.calories=totals['calories']
        user.profile.last_synced_at=latest_end_time
        user.profile.save()
    except Exception as e:
        exc_type, exc_obj, tb = sys.exc_info()
        lineno = tb.tb_lineno
        full_trace = traceback.format_exc()
            
        print(f"Error type: {exc_type.__name__}")
        print(f"Error message: {e}")
        print(f"Line number: {lineno}")
        print("Full traceback:")
        print(full_trace)
        print("Health Checker Failed For User",user.username,e)

def fetch_data_for_all_users():
    users = get_user_model().objects.filter(is_staff=False)
    with ThreadPoolExecutor(max_workers=10) as executor:
        executor.map(fetch_google_data_for_user, users)

def start_checker():
    now = datetime.now()
    next_minute = (now + timedelta(minutes=1)).replace(second=0, microsecond=0)
    scheduler = BackgroundScheduler(jobstores={'default': MemoryJobStore()})
    scheduler.add_job(fetch_data_for_all_users, 'interval', seconds=25,  start_date=next_minute, id='health_checker', replace_existing=True)
    scheduler.start()



        


