from django.urls import path
from . import views

urlpatterns = [
    path('add_resume', views.add_resume, name="Add_Info"),
    path('add_job', views.add_job, name = "Add_jobs")
]