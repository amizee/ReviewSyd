from django.http import HttpResponseRedirect
from django.shortcuts import render, HttpResponse, redirect
from .models import Locations, Faq, Tutor
from django.core.mail import send_mail
from django.contrib import messages
from django.core.files.storage import FileSystemStorage

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


def send_feedback_email(request):
    if request.method == 'POST':
        user_name = request.POST['name']
        user_email = request.POST['email']
        subject = request.POST['subject']
        message = request.POST['message']
        
        # form the message sending to us
        full_message = f"Message from {user_name}\nEmail: {user_email}\n\n{message}"

        # full_message = f"Message from {user_name} <{user_email}>:\n\n{message}"
        print(full_message)
        # Send email
        send_mail(
            subject,
            full_message,
            'shangweiwu1013@gmail.com',  
            ['shangweiwu1013@gmail.com'], 
            fail_silently=False,
        )

        messages.success(request, 'Your feedback has been sent!')
        return redirect('/feedback/')
    return render(request, 'feedback.html')



def findTutor(request):
    tutors = Tutor.objects.all()  # get all tutor objects
    return render(request, "findTutor.html", {'tutors': tutors})


def add_tutor(request):
    if request.method == 'POST':
        # get data from user input
        name = request.POST['name']
        subject = request.POST['subject']
        email = request.POST['email']
        description = request.POST.get('description', '')  # default is empty
        image = request.FILES.get('image', None)
        
        # add a new tutor into database
        tutor = Tutor(name=name, subject=subject, email=email, description=description, image=image)
        tutor.save()

        # redirect to the findTutor page
        return HttpResponseRedirect('/findTutor/')

    # if request is not post, render a blank page or the form page
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