# Generated by Django 4.2.5 on 2023-10-13 03:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0016_alter_locationreviews_location'),
    ]

    operations = [
        migrations.AddField(
            model_name='locations',
            name='nearby',
            field=models.ManyToManyField(blank=True, to='myapp.locations'),
        ),
    ]
