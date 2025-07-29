from datetime import datetime, timedelta
from .models import Reminder
from apscheduler.schedulers.background import BackgroundScheduler
from django.utils import timezone
from Home.models import Reminder
from apscheduler.jobstores.memory import MemoryJobStore
from Buggy.whatsapp_connecter import send_message
def check_reminders():
    now = timezone.localtime().replace(second=0, microsecond=0)
    next_minute = now +timezone.timedelta(minutes=1)
    due_reminders = Reminder.objects.filter(time__gte=now,time__lt=next_minute,is_active=True)
    for reminder in due_reminders:
        send_message({"to":reminder.user.profile.phone_number,"userdata":{"description":reminder.description,"age":reminder.user.profile.age,"prompt":3,"name":reminder.user.username,"language":reminder.user.profile.language}})
        reminder.time += timezone.timedelta(days=1)
        reminder.save()
        

def start():
    now = datetime.now()
    next_minute = (now + timedelta(minutes=1)).replace(second=0, microsecond=0)
    scheduler = BackgroundScheduler(jobstores={'default': MemoryJobStore()})
    scheduler.add_job(check_reminders, 'interval', minutes=1,  start_date=next_minute, id='reminder_checker', replace_existing=True)
    scheduler.start()
