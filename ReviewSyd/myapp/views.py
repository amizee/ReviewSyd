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
    tutors = Tutor.objects.all()  # 查询数据库以获取所有Tutor对象
    return render(request, "findTutor.html", {'tutors': tutors})  # 将tutors传递到模板中

def locationList(request):
    items = Locations.objects.all()
    return render(request, "locationList.html", {"locations": items})
def faq(request):
    faq_items = Faq.objects.all()
    return render(request, "faq.html", {"faq": faq_items})
def location(request, loc):
    location=Locations.objects.get(name=loc)
    return render(request, "location.html", {"location":location})