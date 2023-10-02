from django.http import HttpResponseRedirect
from django.shortcuts import render, HttpResponse
from .models import Locations, Faq, Tutor
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
def findTutor(request):
    return render(request, "findTutor.html")
def findTutor(request):
    tutors = Tutor.objects.all()  # get all tutor objects
    return render(request, "findTutor.html", {'tutors': tutors})

def add_tutor(request):
    if request.method == 'POST':
        # get message from user input
        name = request.POST['name']
        subject = request.POST['subject']
        email = request.POST['email']

        # add a new tutor into database
        tutor = Tutor(name=name, subject=subject, email=email)
        tutor.save()

        # redirect to a new page
        return HttpResponseRedirect('/findTutor/')

    # if request is not post, render a blank page
    return render(request, 'add_tutor.html')

def locationList(request):
    items = Locations.objects.all()
    return render(request, "locationList.html", {"locations": items})
def faq(request):
    faq_items = Faq.objects.all()
    return render(request, "faq.html", {"faq": faq_items})
def location(request, loc):
    location=Locations.objects.get(name=loc)
    return render(request, "location.html", {"location":location})
def accountSettings(request):
    return render(request, "accountSettings.html")
def login(request):
    return render(request, "login.html")
def signup(request):
    return render(request, "signup.html")
def signupCompletion(request):
    return render(request, "signupCompletion.html")