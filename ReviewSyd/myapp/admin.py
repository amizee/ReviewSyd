from django.contrib import admin
from .models import Locations, Faq, Tutor, LocationReviews

# Register your models here.
#python(3) manage.py makemigrations
# python(3) manage.py migrate
admin.site.register(Locations)
admin.site.register(Faq)
admin.site.register(Tutor)
admin.site.register(LocationReviews)