# Generated by Django 4.2.5 on 2023-10-06 03:25

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0008_locationreviews'),
    ]

    operations = [
        migrations.AlterField(
            model_name='locationreviews',
            name='ammenitiesRating',
            field=models.IntegerField(default=0, validators=[django.core.validators.MaxValueValidator(5)]),
        ),
        migrations.AlterField(
            model_name='locationreviews',
            name='cleanlinessRating',
            field=models.IntegerField(default=0, validators=[django.core.validators.MaxValueValidator(5)]),
        ),
        migrations.AlterField(
            model_name='locationreviews',
            name='noisinessRating',
            field=models.IntegerField(default=0, validators=[django.core.validators.MaxValueValidator(5)]),
        ),
    ]
