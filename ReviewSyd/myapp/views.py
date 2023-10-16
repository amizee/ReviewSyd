from venv import logger
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
from django.contrib.auth.hashers import check_password
from django.utils.crypto import get_random_string
from django.utils import timezone
from .models import PasswordResetToken
from .forms import EmailForm, PasswordResetForm
from django.db.models import Q
from django.db.models import Avg




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

@login_required
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
    return render(request, "locationList.html", {"locations": results, "navbar": "locations"})

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
    curr=request.user
    pRev=location.location_reviews.filter(user=curr)
    oRev=location.location_reviews.filter(~Q(user=curr))
    return render(request, "locReviews.html", {"location":location, "pRev":pRev, "oRev":oRev})

@login_required
def subReview(request, loc):
    clean= request.GET.get('clean')
    amen= request.GET.get('amen')
    noise= request.GET.get('noise')
    rev= request.GET.get('rev')
    locID=Locations.objects.get(name=loc)
    curr=request.user
    totRev=locID.location_reviews.all().count()
    if totRev==0:
        avgA=amen
        avgC=clean
        avgN=noise
    else:
        A=locID.avgAmen
        avgA=(A*totRev+int(amen))/(totRev+1)
        C=locID.avgClean
        avgC=(C*totRev+int(clean))/(totRev+1)
        N=locID.avgNoise
        avgN=(N*totRev+int(noise))/(totRev+1)

    locID.avgAmen=avgA
    locID.avgClean=avgC
    locID.avgNoise=avgN
    locID.save(update_fields=['avgNoise', 'avgClean', 'avgAmen'])
    review=LocationReviews(writtenReview = rev, cleanlinessRating = clean, amenitiesRating = amen, noisinessRating = noise, location = locID, user=curr)
    review.save()
    pRev=locID.location_reviews.filter(user=curr)
    oRev=locID.location_reviews.filter(~Q(user=curr))
    return render(request, "locReviews.html", {"location":locID, "pRev":pRev, "oRev":oRev})

def updReview(request, loc):
    val=request.GET.get('val')
    primKey=request.GET.get('pk')
    # Check if 'pk' is present in the URL parameters
    if primKey is None:
        return JsonResponse({'error': '"pk" parameter is missing'}, status=400)

    #int(primKey)
    location=Locations.objects.get(name=loc)
    #logger.info("Location: %s", loc)
    Review=location.location_reviews.get(pk=primKey)#I think the problem is with how primJey is parsed, it is noo
    #logger.info("Primary Key: %s", primKey)
    if int(val)==1:
        l=likes(user=request.user, rev=Review)
        Review.like.add(l.user)
    else:
        Review.like.remove(request.user)
    count= Review.like.count()
    ret=[{'likes': count, 'pk':primKey}]
    return JsonResponse(ret,safe=False)

def delReview(request, loc):
    primKey=request.GET.get('pk')
    if primKey is None:
        return JsonResponse({'error': '"pk" parameter is missing'}, status=400)

    location=Locations.objects.get(name=loc)
    Review=location.location_reviews.get(pk=primKey)
    totRev=location.location_reviews.all().count()
    clean=Review.cleanlinessRating
    amen=Review.amenitiesRating
    noise=Review.noisinessRating
    if totRev==1:
        avgA=0
        avgC=0
        avgN=0
    else:
        A=location.avgAmen
        avgA=(A*totRev-amen)/(totRev-1)
        C=location.avgClean
        avgC=(C*totRev-clean)/(totRev-1)
        N=location.avgNoise
        avgN=(N*totRev-noise)/(totRev-1)

    location.avgAmen=avgA
    location.avgClean=avgC
    location.avgNoise=avgN
    location.save(update_fields=['avgNoise', 'avgClean', 'avgAmen'])
    Review.delete()
    curr=request.user
    pRev=location.location_reviews.filter(user=curr)
    oRev=location.location_reviews.filter(~Q(user=curr))
    return render(request, "locReviews.html", {"location":location, "pRev":pRev, "oRev":oRev})

def repReview(request, loc):
    val=request.GET.get('val')
    primKey=request.GET.get('pk')
    # Check if 'pk' is present in the URL parameters
    if primKey is None:
        return JsonResponse({'error': '"pk" parameter is missing'}, status=400)

    #int(primKey)
    location=Locations.objects.get(name=loc)
    #logger.info("Location: %s", loc)
    Review=location.location_reviews.get(pk=primKey)#I think the problem is with how primJey is parsed, it is noo
    #logger.info("Primary Key: %s", primKey)
    if int(val)==1:
        r=reports(user=request.user, rep=Review)
        Review.report.add(r.user)
    else:
        Review.report.remove(request.user)

    count= Review.report.count()
    ret=[{'pk':primKey}]
    return JsonResponse(ret,safe=False)

@login_required
def accountSettings(request):
    if request.method == 'POST':
        # Check if only verifying the current password
        if 'current_password' in request.POST and 'new_password' not in request.POST:
            current_password = request.POST['current_password']
            user = request.user
            if user.check_password(current_password):
                return JsonResponse({"is_correct": True})
            else:
                return JsonResponse({"is_correct": False, "message": "Incorrect current password."}, status=400)

        # Processing the full form submission:
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        current_password = request.POST['current_password']
        new_password = request.POST['new_password']
        confirm_new_password = request.POST['confirm_new_password']

        # Get the current user
        user = request.user
        
        if not current_password or not new_password or not confirm_new_password:
            return JsonResponse({"success": False, "message": "Passwords cannot be empty."}, status=400)

        # Validate the current password
        if not user.check_password(current_password):
            return JsonResponse({"success": False, "message": "Incorrect current password."}, status=400)

        # Check if the new password matches the confirm password
        if new_password != confirm_new_password:
            return JsonResponse({"success": False, "message": "New password and confirm password do not match."}, status=400)

        # If passwords match, then save the new password
        user.set_password(new_password)

        # Update first name and last name
        user.first_name = first_name
        user.last_name = last_name
        user.save()

        return JsonResponse({"success": True, "message": "Account settings updated successfully!"})

    return render(request, "accountSettings.html", {"current_user": request.user})


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
    return render(request, "UoSList.html", {"UoStudies": results, "navbar": "uos"})

@login_required
def UoSSearch(request):
    search=request.GET.get('search','')
    results=UoS.objects.filter(Q(name__icontains=search) | Q(code__icontains=search))
    res=[{'name':result.name, 'code':result.code} for result in results]
    return JsonResponse(res, safe=False)

@login_required
def UoStudy(request, Uos):
    UoStudy=UoS.objects.get(name=Uos)
    curr=request.user
    pCom=UoStudy.uos_comment.filter(user=curr)
    oCom=UoStudy.uos_comment.filter(~Q(user=curr))
    return render(request, "UoS.html", {"UoS":UoStudy, "pCom":pCom, "oCom":oCom})

@login_required
def subUoS(request, Uos):
    com= request.GET.get('com')
    curr=request.user
    UoStudy=UoS.objects.get(name=Uos)
    comment=UoSComment(user=curr, comment = com, uos = UoStudy)
    comment.save()
    pCom=UoStudy.uos_comment.filter(user=curr)
    oCom=UoStudy.uos_comment.filter(~Q(user=curr))
    return render(request, "UoS.html", {"UoS":UoStudy, "pCom":pCom, "oCom":oCom})

def delUoS(request, Uos):
    primKey=request.GET.get('pk')
    if primKey is None:
        return JsonResponse({'error': '"pk" parameter is missing'}, status=400)
    
    uos=UoS.objects.get(name=Uos)
    com=uos.uos_comment.get(pk=primKey)
    com.delete()
    curr=request.user
    pCom=uos.uos_comment.filter(user=curr)
    oCom=uos.uos_comment.filter(~Q(user=curr))
    return render(request, "UoS.html", {"UoS":uos, "pCom":pCom, "oCom":oCom})

def repUoS(request, Uos):
    val=request.GET.get('val')
    primKey=request.GET.get('pk')
    # Check if 'pk' is present in the URL parameters
    if primKey is None:
        return JsonResponse({'error': '"pk" parameter is missing'}, status=400)

    #int(primKey)
    Unit=UoS.objects.get(name=Uos)
    #logger.info("Location: %s", loc)
    Comment=Unit.location_reviews.get(pk=primKey)#I think the problem is with how primJey is parsed, it is noo
    #logger.info("Primary Key: %s", primKey)
    Comment.reports+=int(val)
    Comment.save(update_fields=['reports'])
    ret=[{'pk':primKey}]
    return JsonResponse(ret,safe=False)

def request_password_reset(request):
    message = ""
    success_message = ""
    if request.method == "POST":
        form = EmailForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            user = User.objects.filter(email=email).first()
            if user:
                token = get_random_string(32)
                expiration_date = timezone.now() + timezone.timedelta(hours=1)
                PasswordResetToken.objects.create(user=user, token=token, expiration_date=expiration_date)
                reset_url = f"http://127.0.0.1:8000/reset-password?token={token}"
                send_mail('Password Reset', f'Click {reset_url} to reset your password.', 'robinwu40@gmail.com', [email])
                success_message = "Reset link successfully sent."
            else:
                message = "This is not a valid email address."
    else:
        form = EmailForm()

    return render(request, 'request_password_reset.html', {'form': form, 'message': message, 'success_message': success_message})




def reset_password(request):
    token = request.GET.get('token')
    if not token:
        print("No token provided.")
        return redirect('request_password_reset')
    
    reset_token = PasswordResetToken.objects.filter(token=token, expiration_date__gte=timezone.now()).first()
    if not reset_token:
        print(f"Invalid or expired token: {token}")
        return render(request, 'invalid_or_expired_token.html')

    if request.method == "POST":
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            new_password = form.cleaned_data.get('new_password')
            confirm_password = form.cleaned_data.get('confirm_password')
            if new_password == confirm_password:
                user = reset_token.user
                user.set_password(new_password)
                user.save()
                reset_token.delete()
                print(f"Password reset successfully for user: {user.username}")
                return redirect('/login/')
            else:
                print("New password and confirm password do not match.")
        else:
            print(f"Form errors: {form.errors}")
    else:
        form = PasswordResetForm()
    return render(request, 'reset_password.html', {'form': form})
