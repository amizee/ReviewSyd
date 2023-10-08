from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, HttpResponse, redirect
from .models import *
from django.core.mail import send_mail
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.shortcuts import get_object_or_404




#python(3) manage.py runserver
# Create your views here.
@login_required
def home(request):
    return render(request, "home.html", {"navbar": "home"})


def ts(request):
    return render(request, "ts.html")


def help(request):
    return render(request, "help.html")


def privacy(request):
    return render(request, "privacy.html")


def feedback(request):
    return render(request, "feedback.html")

def logout_view(request):
    logout(request)
    # Redirect to a success page.
    return redirect('/login/')


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
            'robinwu40@gmail.com',  
            ['robinwu40@gmail.com'], 
            fail_silently=False,
        )

        messages.success(request, 'Your feedback has been sent!')
        return redirect('/feedback/')
    return render(request, 'feedback.html')


@login_required
def findTutor(request):
    tutors = Tutor.objects.all()  # get all tutor objects
    return render(request, "findTutor.html", {'tutors': tutors, "navbar": "tutor"})

@login_required
def add_tutor(request):
    if request.method == 'POST':
        # get data from user input
        name = request.POST['name']
        subject = request.POST['subject']
        email = request.POST['email']
        description = request.POST.get('description', '')  # default is empty
        image = request.FILES.get('image', None)
        
        # add a new tutor into database
        tutor = Tutor(user=request.user, name=name, subject=subject, email=email, description=description, image=image)
        tutor.save()

        # redirect to the findTutor page
        return HttpResponseRedirect('/findTutor/')

    # if request is not post, render a blank page or the form page
    return render(request, 'add_tutor.html')


def remove_tutor(request, tutor_id):
    # tutor to be remove
    tutor = get_object_or_404(Tutor, id=tutor_id)

    # insure to be the creator
    if request.user == tutor.user:
        tutor.delete()
    
    return redirect('findTutor')  

@login_required
def locationList(request):
    results=Locations.objects.all()
    return render(request, "locationList.html", {"locations": results})

@login_required
def locSearch(request):
    search=request.GET.get('search','')
    results=Locations.objects.filter(name__icontains=search)
    res=[{'name':result.name} for result in results]
    return JsonResponse(res, safe=False)

def faq(request):
    faq_items = Faq.objects.all()
    return render(request, "faq.html", {"faq": faq_items})

@login_required
def location(request, loc):
    location=Locations.objects.get(name=loc)
    return render(request, "location.html", {"location":location})

@login_required
def locReviews(request, loc):
    location=Locations.objects.get(name=loc)
    return render(request, "locReviews.html", {"location":location})

@login_required
def subReview(request, loc):
    clean= request.GET.get('clean')
    amen= request.GET.get('amen')
    noise= request.GET.get('noise')
    rev= request.GET.get('rev')
    loc=request.GET.get('loc')
    locID=Locations.object.get(name=loc)
    review=LocationReview(reviewerSID = 0, writtenReview = rev, cleanlinessRating = clean, amenitiesRating = amen, noisinessRating = noise, location = loc)
    review.save()
    location=Locations.objects.get(name=loc)
    return render(request, "locReviews.html", {"location":location})

@login_required
def accountSettings(request):
    return render(request, "accountSettings.html")


def login_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        # Django authenticaiton
        user = authenticate(request, username=email, password=password)
        
        if user is not None:
            auth_login(request, user)
            print('Yes')
            return redirect('/')
        else:
            print('No')
            messages.error(request, 'Invalid email or password !!')
    return render(request, 'login.html')


def signup(request):
    if request.method == "POST":
        first_name = request.POST['first_name']
        surname = request.POST['surname']
        email = request.POST['email'] + "@uni.sydney.edu.au"
        if User.objects.filter(username=email).exists():
            # This email (username) is already taken
            messages.error(request, 'The email address is already in use.')
            return redirect('signup')  # Redirect back to the signup page
        password = request.POST['password']

        # create a new user
        user = User.objects.create_user(username=email, email=email, password=password, first_name=first_name, last_name=surname)

        # create a userprofile
        # user_profile = UserProfile(
        #     user=user,
        #     first_name=first_name,
        #     surname=surname,
        #     email=email,
        # )
        user_profile = UserProfile(user=user)
        user_profile.save()

        return redirect('/login/')  # rederict to sign in page
    return render(request, "signup.html")


@login_required
def signupCompletion(request):
    return render(request, "signupCompletion.html")

@login_required
def UoSList(request):
    results=UoS.objects.all()
    return render(request, "UoSList.html", {"UoS": results})

@login_required
def UoSSearch(request):
    search=request.GET.get('search','')
    results=UoS.objects.filter(name__icontains=search)
    res=[{'name':result.name} for result in results]
    return JsonResponse(res, safe=False)

@login_required
def UoStudy(request, UoS):
    UoS=UoS.objects.get(name=UoS)
    return render(request, "UoS.html", {"UoS":UoS})

@login_required
def subComment(request, UoS):
    com= request.GET.get('com')
    UoS=request.GET.get('UoS')
    UoS=Locations.object.get(name=UoS)
    comment=UoSComment(reviewerSID = 0, comment = com, UoS = UoS)
    comment.save()
    UoS=UoS.objects.get(name=UoS)
    return render(request, "UoS.html", {"UoS":UoS})