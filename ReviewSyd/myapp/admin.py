from django.contrib import admin
from .models import Locations
# Register your models here.
#python(3) manage.py makemigrations
# python(3) manage.py migrate
admin.site.register(Locations)