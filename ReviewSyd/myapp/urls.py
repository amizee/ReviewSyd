from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns=[
    path("", views.home, name="home"),
    path("terms-and-conditions/", views.ts, name="terms and conditions",),
    path("help/", views.help, name="help"),
    path("privacy/", views.privacy, name="privacy"),
    path("feedback/", views.feedback, name="feedback"),
    path('send_feedback/', views.send_feedback_email, name='send_feedback'),
    path("locationList/", views.locationList, name="location list"),
    path("locationList/search/", views.LLsearch, name="location_list_search"),
    path("faq/", views.faq, name="faq"),
    path('add_tutor/', views.add_tutor, name='add_tutor'),
    path("findTutor/", views.findTutor, name="findTutor"),
    path("location/<str:loc>/", views.location, name="location"),
    path("accountSettings/", views.accountSettings, name="account settings"), 
    path("login/", views.login, name="login"), 
    path("signup/", views.signup, name="signup"), 
    path("signupCompletion/", views.signupCompletion, name="signupCompletion"), 
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
