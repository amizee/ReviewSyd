from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator


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

class LocationReviews(models.Model):
    reviewerSID = models.IntegerField()
    writtenReview = models.CharField(max_length=255)
    likes = models.IntegerField(default=0)
    cleanlinessRating = models.IntegerField(validators=[MaxValueValidator(5)],default=0)
    amenitiesRating = models.IntegerField(validators=[MaxValueValidator(5)],default=0)
    noisinessRating = models.IntegerField(validators=[MaxValueValidator(5)],default=0)
    reports = models.IntegerField(default=0)
    location = models.ForeignKey(Locations, on_delete=models.CASCADE, related_name='reviews')


class Faq(models.Model):
    question = models.CharField(max_length=250)
    answer = models.CharField(max_length=1000)

class Reviews(models.Model):
    name=models.CharField(max_length=255)


class Tutor(models.Model):
    name = models.CharField(max_length=100)
    subject = models.CharField(max_length=100)
    email = models.EmailField()
    description = models.TextField(blank=True) 
    image = models.ImageField(upload_to='tutor_images/', blank=True) 

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    student_id = models.IntegerField(blank=False, default=0)
    username = models.CharField(max_length=25)
    email = models.EmailField(max_length=100)
    is_tutor = models.BooleanField(default=False)
