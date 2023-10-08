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
    path("locationList/search/", views.locSearch, name="loc_search"),
    path("faq/", views.faq, name="faq"),
    path('add_tutor/', views.add_tutor, name='add_tutor'),
    path("findTutor/", views.findTutor, name="findTutor"),
    path("location/<str:loc>/", views.location, name="location"),
    path("location/<str:loc>/reviews/", views.locReviews, name="locReviews"),
    path("location/<str:loc>/reviews/submit/", views.subReview, name="subReview"),
    path("accountSettings/", views.accountSettings, name="account settings"), 
    path('login/', views.login_view, name='login_view'),
    path("signup/", views.signup, name="signup"), 
    path("signupCompletion/", views.signupCompletion, name="signupCompletion"), 
    path("UoSList/", views.UoSList, name="UoSList"),
    path("UoSList/search/", views.UoSSearch, name="UoS_search"),
    path("UoS/<str:UoS>/", views.UoStudy, name="UoS"),  
    path('logout/', views.logout_view, name='logout_view'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
