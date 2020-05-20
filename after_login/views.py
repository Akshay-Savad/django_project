from django.shortcuts import render, redirect
from django.http import HttpResponse
import mysql.connector
from django.contrib import messages

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="pbl1"
)

mycursor = mydb.cursor()

# Create your views here.


def add_resume(request):
    if request.method == 'POST':
        name = request.POST["username"]
        job_des = request.POST["job_description"]
        skill = request.POST["skill"]
        education = request.POST["education"]
        experience = request.POST["experience"]
        email = request.POST["email"]

        sql = "INSERT INTO resume (applicant_name, job_description, skill, education, experience, email) VALUES (%s, %s, %s, %s, %s, %s)"
        val = (name, job_des, skill, education, experience, email)
        mycursor.execute(sql, val)
        mydb.commit()

        messages.info(request, "Job Entered Successfully")
        return redirect("/")

    else:
        return render(request, 'add_resume.html')


def add_job(request):
    if request.method == 'POST':
        company = request.POST["company"]
        job_des = request.POST["job_des"]
        location = request.POST["location"]
        duration = request.POST["duration"]
        salary = request.POST["salary"]
        addBy = request.COOKIES.get("login")

        sql = "INSERT INTO jobs (company_name, job_description, location, duration, salary, addBy) VALUES (%s, %s, %s, %s, %s, %s)"
        val = (company, job_des, location, duration, salary, addBy)

        mycursor.execute(sql, val)
        mydb.commit()

        messages.info(request, "Job Resume Successfully")
        return redirect("/")

    else:
        return render(request, 'add_job.html')
