from django.urls import path
from . import views

urlpatterns = [
    path('signup_HR', views.signup_HR, name = 'signup_HR'),
    path('signup_applicant', views.signup_app, name = 'signup'),
]