from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15, null=False, blank=False)
    profile_image = models.ImageField(upload_to="profile/", verbose_name="Profile Pic", default="profile/default.png")
    token = models.CharField(max_length=255, null=False, blank=False, default="")
    refresh_token = models.CharField(max_length=255, null=False, blank=False, default="")
    token_uri = models.CharField(max_length=255, null=False, blank=False, default="")
    client_id = models.CharField(max_length=255, null=False, blank=False, default="")
    client_secret = models.CharField(max_length=255, null=False, blank=False, default="")
    age = models.CharField(max_length=3, default="21", blank=False, null=False)
    language = models.CharField(max_length=30, default="English", blank=False, null=False)
    last_synced_at = models.BigIntegerField(default=0)
    heart_rate = models.IntegerField(default=0)
    step_count = models.IntegerField(default=0)
    calories = models.IntegerField(default=0)

class Notifications(models.Model):
    NOTIFICATION_TYPES = (
        ('info', 'Info'),
        ('warning', 'Warning'),
        ('error', 'Error'),
    )
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    message = models.TextField()
    notification_type = models.CharField(max_length=10, choices=NOTIFICATION_TYPES, default='info')
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    def __str__(self):
        return f"{self.user.username} - {self.notification_type} - {self.message[:20]}"

class Reminder(models.Model):
    description = models.TextField()
    time = models.DateTimeField()
    recurrence = models.CharField(max_length=50, blank=True, null=True)  # e.g., 'daily', 'every monday'
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
