from django.shortcuts import render, HttpResponse
from .models import Locations
#python(3) manage.py runserver
# Create your views here.
def home(request):
    return render(request, "home.html")
def ts(request):
    return render(request, "ts.html")
def help(request):
    return render(request, "help.html")
def privacy(request):
    return render(request, "privacy.html")
def feedback(request):
    return render(request, "feedback.html")
def locationList(request):
    items = Locations.objects.all()
    return render(request, "locationList.html", {"locations": items})
def faq(request):
    return render(request, "faq.html")