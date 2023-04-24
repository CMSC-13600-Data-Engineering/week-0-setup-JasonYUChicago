from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.template import loader
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from .models import*

def index(request):
    return render(request, 'app/index.html', {"test":"SUCCESS!",
                                              "title":"Jason and Victoria's app"})

#Login Page:
def loginForm(request, error_msg=''):
    return render(request,'registration/login.html', {'error':error_msg})

def login(request):
    email = request.POST['email']
    password = request.POST['pwd']
    user = authenticate(request,email=email, password=password)
    if user is not None:
        login(request,user)
        return render(request, 'app/success.html')
    return loginForm(request, error_msg='did not work')

#ADDING INSTRUCTORS

def addUserForm(request, error_msg=''):
    return render(request, 'app/register.html', {'error':error_msg})

def handleUserForm(request):
    #if request.method != "POST":
    #    return HttpResponse("Error: the request is not an HTTP POST request\n", status=500)
    #print(str(request.POST))
    type = 'Instructor'
    #type = request.POST['role']

    if(type=='Instructor'):
        try:
            first_name = request.POST['fn']
            last_name = request.POST['ln']
            email = request.POST['email']
            password = request.POST['pwd']
        except:
            return addUserForm(request, error_msg='Please fill out all the fields of the form')
        try:
            addInstructor(first_name,last_name,email,password)
        except Exception as e:
            return addUserForm(request, error_msg='Error: There is a database error in adding this Instructor: ' + str(e))
        Instructor = authenticate(request, email=email, password=password)
        if Instructor is not None:
            login(request,Instructor)
            return render(request, 'app/success.html')
        else:
            return addUserForm(request, error_msg='Could Not Log you In!')
    
    elif(type == 'Student'):
        try:
            first_name = request.POST['fn']
            last_name = request.POST['ln']
            email = request.POST['email']
            password = request.POST['pwd']
        except:
            return addUserForm(request, error_msg='Please fill out all the fields of the form')
        try:
            addStudent(first_name,last_name,email,password)
        except Exception as e:
            return addUserForm(request, error_msg='Error: There is a database error in adding this Student '+ str(e))
        return addUserForm(request, 'You have successfully signed up as a student!')
    else:
        return addUserForm(request, 'it didnt work')




#THE /app/create VIEW

def addCourseForm(request, error_msg=''):
    return render(request, 'app/course.html', {'error':error_msg})
    
def handleCourseForm(request, error_msg=''):
    if request.method != "POST":
        return HttpResponse("Error: the request is not an HTTP POST request\n", status=500)
    print(str(request.POST))

    try:
        course_name = request.POST['name']
        course_number = request.POST['num']
        Instructor_id = request.POST['in_id']
        start = request.POST['start']
        end = request.POST['end']
        meet_time = request.POST['meet_time']
    except:
        return addCourseForm(request,erorr_msg="Please fill out all the fields in the form")
    
#    if Course.objects.filter(Instructor_id=Instructor_id):

    try:
        addCourse(course_name,course_number,Instructor_id,start,end,meet_time)
    except Exception as e:
        return addCourseForm(request, error_msg='Error: There is a database error in adding this Course ' + str(e))
    return render(request,'app/course/course_created.html',{'error':error_msg})

def course_created(request, error_msg=''):
    return render(request,'app/course_created.html',{'error':error_msg})
