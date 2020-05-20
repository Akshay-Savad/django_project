from django.shortcuts import render, redirect
from django.contrib import messages
import mysql.connector

# Create your views here.
mydb = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "root",
    database = "pbl1"    
    )

mycursor = mydb.cursor()

def signup_HR(request):
    
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        des = str('HR')

        sql = "SELECT name FROM login_user"
        mycursor.execute(sql)
        result = mycursor.fetchall()

        flag = 0

        for x in result:
            if x[0] == username:
                flag = 1


        if flag == 1:        
            messages.info(request, "Username taken")
            return render(request, 'signup_HR.html')


        else:    
            sql = "INSERT INTO login_user (name, password, position) VALUES (%s, %s, %s)"
            val = (username, password, des)
            mycursor.execute(sql, val)
            mydb.commit()

            return redirect('/')        


    else:  
        return render(request, 'signup_HR.html')

def signup_app(request):
    
    if request.method == 'POST':
        username = request.POST['uname']
        password = request.POST['password']
        des = str('seek')

        sql = "SELECT name FROM login_user"
        mycursor.execute(sql)
        result = mycursor.fetchall()

        flag = 0

        for x in result:
            if x[0] == username:
                flag = 1


        if flag == 1:        
            messages.info(request, "Username taken")
            return render(request, 'signup_applicant.html')
        else:    
            sql = "INSERT INTO login_user (name, password, position) VALUES (%s, %s, %s)"
            val = (username, password, des)
            mycursor.execute(sql, val)
            mydb.commit()


            return redirect('/')     
    else:        
        return render(request, 'signup_applicant.html')