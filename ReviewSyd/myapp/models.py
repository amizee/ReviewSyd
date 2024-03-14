from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator


# Create your models here.
class Amenity(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='amenities_images/', blank=True)

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
    nearby = models.ManyToManyField('self', blank=True)
    image = models.ImageField(upload_to='location_images/', blank=True)
    amenities=models.ManyToManyField(Amenity, blank=True)
    avgOverall=models.IntegerField(blank=True, default=0)

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    student_id = models.IntegerField(blank=False, default=0)
    is_tutor = models.BooleanField(default=False)



class LocationReviews(models.Model):
    writtenReview = models.CharField(max_length=255)
    like=models.ManyToManyField(User, through='likes', related_name='rev_likes')
    cleanlinessRating = models.IntegerField(validators=[MaxValueValidator(5)],default=0)
    amenitiesRating = models.IntegerField(validators=[MaxValueValidator(5)],default=0)
    noisinessRating = models.IntegerField(validators=[MaxValueValidator(5)],default=0)
    report=models.ManyToManyField(User, through='reports', related_name='rev_reports')
    location = models.ForeignKey(Locations, on_delete=models.CASCADE, related_name='location_reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

class likes(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='user_like')
    rev = models.ForeignKey(LocationReviews, on_delete=models.CASCADE, null=True, blank=True, related_name='rev_like')

class reports(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='user_rep')
    rep = models.ForeignKey(LocationReviews, on_delete=models.CASCADE, null=True, blank=True, related_name='rev_rep')    

class UoS(models.Model):
    code = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)

class UoSComment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    comment = models.CharField(max_length=255)
    uos = models.ForeignKey(UoS, on_delete=models.CASCADE, related_name='uos_comment', null=True, blank=True)
    report=models.ManyToManyField(User, through='UoSRep', related_name='uos_reports')

class UoSRep(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='uos_rep')
    rep = models.ForeignKey(UoSComment, on_delete=models.CASCADE, null=True, blank=True, related_name='uos_rep')  

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

class PasswordResetToken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=64)
    expiration_date = models.DateTimeField()
