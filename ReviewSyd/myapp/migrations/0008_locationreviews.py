# Generated by Django 4.2.5 on 2023-10-06 03:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0007_userprofile'),
    ]

    operations = [
        migrations.CreateModel(
            name='LocationReviews',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reviewerSID', models.IntegerField()),
                ('writtenReview', models.CharField(max_length=255)),
                ('likes', models.IntegerField(default=0)),
                ('cleanlinessRating', models.IntegerField(default=0)),
                ('ammenitiesRating', models.IntegerField(default=0)),
                ('noisinessRating', models.IntegerField(default=0)),
                ('reports', models.IntegerField(default=0)),
                ('location', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='myapp.locations')),
            ],
        ),
    ]