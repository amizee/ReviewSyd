# Generated by Django 4.2.5 on 2023-10-08 08:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0010_rename_ammenitiesrating_locationreviews_amenitiesrating'),
    ]

    operations = [
        migrations.CreateModel(
            name='UoS',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=255)),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='UoSComment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('SID', models.IntegerField()),
                ('comment', models.CharField(max_length=255)),
            ],
        ),
    ]
