from django.db import models

# Create your models here.
class Locations(models.Model):
    name= models.CharField(max_length=255)
    location= models.CharField(max_length=255)
    hours=models.CharField(max_length=255)
    website=models.CharField(max_length=255, blank=True)
    phone_number=models.CharField(max_length=255, blank=True)
    amenities=models.CharField(max_length=255, blank=True)
    avgNoise=models.IntegerField(blank=True, default=0)
    avgAmen=models.IntegerField(blank=True, default=0)
    avgClean=models.IntegerField(blank=True, default=0)
    nearPlaces=models.CharField(max_length=255, blank=True)

class Faq(models.Model):
    question = models.CharField(max_length=250)
    answer = models.CharField(max_length=1000)

class Reviews(models.Model):
    name=models.CharField(max_length=255)


class Tutor(models.Model):
    name = models.CharField(max_length=100)
    subject = models.CharField(max_length=100)
    email = models.EmailField()
    