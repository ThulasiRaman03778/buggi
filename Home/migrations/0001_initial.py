# Generated by Django 5.1.4 on 2025-05-13 09:50

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Notifications',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.TextField()),
                ('notification_type', models.CharField(choices=[('info', 'Info'), ('warning', 'Warning'), ('error', 'Error')], default='info', max_length=10)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('is_read', models.BooleanField(default=False)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notifications', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone_number', models.CharField(max_length=15)),
                ('profile_image', models.ImageField(default='profile/default.png', upload_to='profile/', verbose_name='Profile Pic')),
                ('token', models.CharField(default='', max_length=255)),
                ('refresh_token', models.CharField(default='', max_length=255)),
                ('token_uri', models.CharField(default='', max_length=255)),
                ('client_id', models.CharField(default='', max_length=255)),
                ('client_secret', models.CharField(default='', max_length=255)),
                ('age', models.CharField(default='21', max_length=3)),
                ('language', models.CharField(default='English', max_length=30)),
                ('last_synced_at', models.BigIntegerField(default=0)),
                ('heart_rate', models.IntegerField(default=0)),
                ('step_count', models.IntegerField(default=0)),
                ('calories', models.IntegerField(default=0)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Reminder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField()),
                ('time', models.DateTimeField()),
                ('recurrence', models.CharField(blank=True, max_length=50, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
