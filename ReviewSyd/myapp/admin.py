from django.contrib import admin
from .models import *

# Register your models here.
#python(3) manage.py makemigrations
# python(3) manage.py migrate
admin.site.register(Locations)
admin.site.register(Faq)
admin.site.register(Tutor)
admin.site.register(LocationReviews)
admin.site.register(UserProfile)
admin.site.register(UoS)
admin.site.register(UoSComment)
admin.site.register(Amenity)