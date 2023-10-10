from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator


class Amenity(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='amenities_images/', blank=True)
# Create your models here.
class Locations(models.Model):
    name= models.CharField(max_length=255)
    location= models.CharField(max_length=255)
    hours=models.CharField(max_length=255)
    website=models.CharField(max_length=255, blank=True)
    phone_number=models.CharField(max_length=255, blank=True)
    amenities=models.ManyToManyField(Amenity, blank=True)
    avgNoise=models.IntegerField(blank=True, default=0)
    avgAmen=models.IntegerField(blank=True, default=0)
    avgClean=models.IntegerField(blank=True, default=0)
    nearPlaces=models.CharField(max_length=255, blank=True)
    image = models.ImageField(upload_to='location_images/', blank=True)


class LocationReviews(models.Model):
    reviewerSID = models.IntegerField()
    writtenReview = models.CharField(max_length=255)
    likes = models.IntegerField(default=0)
    cleanlinessRating = models.IntegerField(validators=[MaxValueValidator(5)],default=0)
    amenitiesRating = models.IntegerField(validators=[MaxValueValidator(5)],default=0)
    noisinessRating = models.IntegerField(validators=[MaxValueValidator(5)],default=0)
    reports = models.IntegerField(default=0)
    location = models.ForeignKey(Locations, on_delete=models.CASCADE, related_name='reviews')

class UoS(models.Model):
    code = models.CharField(max_length=255)
    name = models.CharField(max_length=255)

class UoSComment(models.Model):
    commenterSID = models.IntegerField(default=0)
    comment = models.CharField(max_length=255)
    uos = models.ForeignKey(UoS, on_delete=models.CASCADE, related_name='comments', default=0)


class Faq(models.Model):
    question = models.CharField(max_length=250)
    answer = models.CharField(max_length=1000)

class Reviews(models.Model):
    name=models.CharField(max_length=255)


class Tutor(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100)
    subject = models.CharField(max_length=100)
    email = models.EmailField()
    description = models.TextField(blank=True) 
    image = models.ImageField(upload_to='tutor_images/', blank=True) 


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    student_id = models.IntegerField(blank=False, default=0)
    is_tutor = models.BooleanField(default=False)


class PasswordResetToken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=64)
    expiration_date = models.DateTimeField()
