# Generated by Django 4.2.5 on 2023-10-12 06:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('myapp', '0017_locationreviews_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='locationreviews',
            name='reviewerSID',
        ),
        migrations.RemoveField(
            model_name='locationreviews',
            name='likes',
        ),
        migrations.AddField(
            model_name='locationreviews',
            name='likes',
            field=models.ManyToManyField(blank=True, related_name='rev_likes', through='myapp.Likes', to=settings.AUTH_USER_MODEL),
        ),
    ]
