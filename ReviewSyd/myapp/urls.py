from django.urls import path
from . import views

urlpatterns=[
    path("", views.home, name="home"),
    path("terms-and-conditions/", views.ts, name="terms and conditions",),
    path("help/", views.help, name="help"),
    path("privacy/", views.privacy, name="privacy"),
    path("feedback/", views.feedback, name="feedback"),
    path("locationList/", views.locationList, name="location list"),
    path("faq/", views.faq, name="faq"),
    path("findTutor/", views.findTutor, name="findTutor"),
    path("location/<str:loc>/", views.location, name="location"),
]