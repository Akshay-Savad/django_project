from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse, HttpRequest
import mysql.connector
from django.template import loader

# Create your views here.

# styling of results that coming from database


def style(x):
    temp = str(x)
    lenght = len(temp)
    x = temp.capitalize()
    return x


def login(request):
    # making database Connection
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="pbl1"
    )

    mycursor = mydb.cursor()

    sql = "SELECT job_description FROM jobs"
    mycursor.execute(sql)
    result = mycursor.fetchall()

    domain_lst = []
    for x in result:
        temp = style(x[0])
        domain_lst.append(temp)

    mycursor = mydb.cursor()
    sql = "SELECT job_description FROM resume"
    mycursor.execute(sql)
    result = mycursor.fetchall()

    for x in result:
        temp = style(x[0])
        domain_lst.append(temp)

    domain_lst = list(dict.fromkeys(domain_lst))

    return render(request, "login.html", {'domain': domain_lst})


def after_login(request):
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="pbl1"
    )

    if request.method == "GET":
        return redirect('/')
    else:
        username = request.POST['username']
        password = request.POST["password"]
        flag = int(0)

        mycursor = mydb.cursor()
        sql = "SELECT name FROM login_user"
        mycursor.execute(sql)
        result = mycursor.fetchall()

        for res in result:
            if username == res[0]:
                flag = 1
                break

        if flag == 1:
            mycursor = mydb.cursor()
            sql = "SELECT password FROM login_user WHERE name = %s"
            adr = (username,)
            mycursor.execute(sql, adr)
            result = mycursor.fetchall()
            for res in result:
                res1 = res[0]

            if password != res1:
                messages.info(request, "Wrong Password")
                return redirect('/')

            else:
                # for recognizing user from its username
                mycursor = mydb.cursor()
                sql = "SELECT position FROM login_user WHERE name = %s"
                adr = (username,)
                mycursor.execute(sql, adr)
                result = mycursor.fetchall()
                des = str()
                for x in result:
                    des = style(x[0])
                job = request.POST['job_description']

                # seek means applicant
                if des == 'Seek':
                    mycursor = mydb.cursor()
                    sql = "SELECT * FROM jobs WHERE job_description = %s"
                    adr = (job,)
                    mycursor.execute(sql, adr)
                    result = mycursor.fetchall()

                    jobs_list = []
                    for x in result:
                        temp = {}
                        temp["company_name"] = x[1]
                        temp["job_des"] = x[2]
                        temp["location"] = x[3]
                        temp["duration"] = x[4]
                        temp["money"] = x[5]

                        jobs_list.append(temp)

                    temp_obj = render(request, "Jobs.html", {"des": jobs_list})

                    # Setting cookie
                    response = HttpResponse(temp_obj)
                    response.set_cookie('login', username, max_age=None)

                    return response

                else:
                    resume_list1 = []

                    mydb = mysql.connector.connect(
                        host="localhost",
                        user="root",
                        password="root",
                        database="pbl1"
                    )

                    mycursor = mydb.cursor()
                    sql = "SELECT * FROM resume WHERE job_description = %s"
                    adr = (job,)
                    mycursor.execute(sql, adr)
                    result = mycursor.fetchall()

                    for x in result:
                        temp = {}
                        temp["applicant_name"] = x[1]
                        temp["domain"] = x[2]
                        temp["skill"] = x[3]
                        temp["education"] = x[4]
                        temp["experience"] = x[5]
                        temp["email"] = x[6]

                        resume_list1.append(temp)

                    print(resume_list1)
                    myObj = render(request, "HR.html", {'des': resume_list1})

                    # Setting cookie
                    response = HttpResponse(myObj)
                    response.set_cookie('login', username, max_age=None)

                    return response

        else:
            messages.info(request, "Wrong Username")
            return redirect('/')


def uploadedJob(request):
    login_name = request.COOKIES.get('login')
    job_list = []

    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="pbl1"
    )
    mycursor = mydb.cursor()
    sql = "SELECT * FROM jobs WHERE addBy = %s"
    adr = (login_name,)
    mycursor.execute(sql, adr)
    result = mycursor.fetchall()

    for x in result:
        temp = {}
        temp["company_name"] = x[1]
        temp["job_description"] = x[2]
        temp["location"] = x[3]
        temp["duration"] = x[4]
        temp["salary"] = x[5]
        temp["id"] = x[0]

        job_list.append(temp)

    return render(request, "uploadedJob.html", {"job_list": job_list})


# def deleteJob(request, user_id):
def specific_request(request, pk):
    user_id = pk
    user_id = int(user_id)
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="pbl1"
    )
    mycursor = mydb.cursor()
    sql = "DELETE FROM jobs WHERE id = %s"
    adr = (user_id,)
    mycursor.execute(sql, adr)
    mydb.commit()

    login_name = request.COOKIES.get('login')
    job_list = []

    mycursor = mydb.cursor()
    sql = "SELECT * FROM jobs WHERE addBy = %s"
    adr = (login_name,)
    mycursor.execute(sql, adr)
    result = mycursor.fetchall()

    temp = {}
    for x in result:
        temp["company_name"] = x[1]
        temp["job_description"] = x[2]
        temp["location"] = x[3]
        temp["duration"] = x[4]
        temp["salary"] = x[5]
        temp["id"] = x[0]

        job_list.append(temp)

    if len(job_list) != 0:
        messages.info(request, "Job Removd Succesfully")
        return redirect("/")
    else:
        messages.info(request, "All jobs are removed that you uploaded")
        return redirect("/")
