# Generated by Django 4.2.5 on 2023-10-12 06:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0017_locationreviews_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='locationreviews',
            name='reviewerSID',
        ),
    ]
