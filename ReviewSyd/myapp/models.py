from django.db import models

# Create your models here.
class Locations(models.Model):
    name= models.CharField(max_length=200)
    location= models.CharField(max_length=200)
    hours=models.CharField(max_length=200)
    website=models.CharField(max_length=200, blank=True, default='')
    phone_number=models.CharField(max_length=200, blank=True, default='')

class Faq(models.Model):
    question = models.CharField(max_length=250)
    answer = models.CharField(max_length=1000)
    