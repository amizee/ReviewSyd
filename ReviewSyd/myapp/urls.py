from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns=[
    path("", views.locationList, name="location list"),
    path("terms-and-conditions/", views.ts, name="terms and conditions",),
    path("help/", views.help, name="help"),
    path("privacy/", views.privacy, name="privacy"),
    path("feedback/", views.feedback, name="feedback"),
    path('send_feedback/', views.send_feedback_email, name='send_feedback'),
    path("locationsMap/", views.locationsMap, name="locationsMap"),
    path("locationList/search/", views.locSearch, name="loc_search"),
    path("faq/", views.faq, name="faq"),
    path('add_tutor/', views.add_tutor, name='add_tutor'),
    path("findTutor/", views.findTutor, name="findTutor"),
    path('remove_tutor/<int:tutor_id>/', views.remove_tutor, name='remove_tutor'),
    path("location/<str:loc>/", views.location, name="location"),
    path("location/<str:loc>/reviews/", views.locReviews, name="locReviews"),
    path("location/<str:loc>/reviews/submit/", views.subReview, name="subReview"),
    path("location/<str:loc>/reviews/like/", views.updReview, name="updReview"), #this used to be "subReview why?"
    path("location/<str:loc>/reviews/del/", views.delReview, name="delReview"),
    path("location/<str:loc>/reviews/rep/", views.repReview, name="repReview"),
    path("accountSettings/", views.accountSettings, name="accountSettings"), 
    path('login/', views.login_view, name='login_view'),
    path("signup/", views.signup, name="signup"), 
    path("signupCompletion/", views.signupCompletion, name="signupCompletion"), 
    path("UoSList/", views.UoSList, name="UoSList"),
    path("UoSList/search/", views.UoSSearch, name="UoS_search"),
    path("UoS/<str:Uos>/", views.UoStudy, name="UoS"),  
    path("UoS/<str:Uos>/submit/", views.subUoS, name="subUoS"),
    path("UoS/<str:Uos>/del/", views.delUoS, name="delUoS"),
    path("UoS/<str:Uos>/rep/", views.repUoS, name="repUoS"),
    path('logout/', views.logout_view, name='logout_view'),
    path('request-password-reset/', views.request_password_reset, name='request_password_reset'),
    path('reset-password/', views.reset_password, name='reset_password'),
    path('verify_email/', views.verify_email, name="verify_email"),
    path('check_verification_code/', views.check_verification_code, name='check_verification_code'),
    path('update_name/', views.update_name, name='updateName'),
    path('verify_current_password/', views.verify_current_password, name='verify_current_password'),
    path('update_password/', views.update_password, name='update_password'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
