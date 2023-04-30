from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.template import loader
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import*
from datetime import datetime
import random, string

def index(request):
    return render(request, 'app/index.html', {"test":"SUCCESS!",
                                              "title":"Jason and Victoria's app"})

#Login Page:
def loginForm(request, error_msg=''):
    return render(request,'app/login.html', {'error':error_msg})

def make_login(request):
    email = request.POST['email']
    password = request.POST['pwd']
    user = authenticate(username=email, password=password)
    if user is not None:
        login(request,user)
        return render(request, 'app/course.html')
    else:
        return loginForm(request, error_msg='did not work')

#Logout:
def logout_view(request):
    logout(request)
    return loginForm(request,'You have just logged out!')
    

#ADDING INSTRUCTORS

def addUserForm(request, error_msg=''):
    return render(request, 'app/register.html', {'error':error_msg})

def handleUserForm(request):
    #if request.method != "POST":
    #    return HttpResponse("Error: the request is not an HTTP POST request\n", status=500)
    #print(str(request.POST))
    type = 'Student'
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
        try:
            user = authenticate(username=email, password=password)
            if user is not None:
                login(request,user)
                return redirect(handleCourseForm)
        except Exception as e: 
            return addUserForm(request,error_msg='Error: The login in not working')
#        return addUserForm(request, error_msg='Could Not Log you In!')
    
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
        try:
            user = authenticate(username=email, password=password)
            if user is not None:
                login(request,user)
                return render(request, 'app/success.html')
            else:
                return loginForm(request, error_msg='did not work')
        except Exception as e: 
            return addUserForm(request,error_msg='Error: The login in not working')
    else:
        return addUserForm(request, 'it didnt work')




#THE /app/create VIEW

def addCourseForm(request, error_msg=''):
    return render(request, 'app/course.html', {'error':error_msg})
    
def handleCourseForm(request):
    #if request.method != "POST":
    #    return HttpResponse("Error: the request is not an HTTP POST request\n", status=500)
    #print(str(request.POST)

    try:
        Instructor_id = Instructor.objects.get(email=request.user.email)
    except:
        return addCourseForm(request,error_msg='You are not logged in as an instructor. Please log in.')

    try:
        course_name = request.POST['course_name']
        course_number = request.POST['course_number']
        start = request.POST['start']
        end = request.POST['end']
        meet_days = request.POST['meet_days']
        meet_start = request.POST['meet_start']
        meet_end = request.POST['meet_end']
    except Exception as e:
        return addCourseForm(request,error_msg='please fill out all the fields of the form')
    
    #first check is in the models.py page

    #checks if instructor is already teaching a class during the input time period
    for course in Course.objects.filter(instructor_id=Instructor_id):
        old_start = course.meet_start_time
        old_end = course.meet_end_time
        if not ((meet_start>old_end and meet_end>old_end) or (meet_start<old_start and meet_end<old_start)):
            return addCourseForm(request,error_msg='You are already teaching a class from '+ old_start + ' ' + old_end)

    #checks if input start date is after end date
    start_date = datetime.strptime(start, '%Y-%m-%d')
    end_date = datetime.strptime(end,'%Y-%m-%d')
    if start_date>end_date:
        return addCourseForm(request, error_msg='The start date cannot be later than the end date')
    
    #checks if start time is after end time
    if meet_start>meet_end:
        return addCourseForm(request, error_msg='The start time cannot be later than the end time- unless it is a midnight class')
    
    try:
        addCourse(course_name,course_number,Instructor_id,start,end,meet_days,meet_start,meet_end)
    except Exception as e:
        return addCourseForm(request, error_msg='Error: There is a database error in adding this Course ' + str(e))
    return course_created(request,course_number)

def course_created(request, error_msg='',course_number=''):
    return render(request,'app/course_created.html',{
        'error':error_msg,
        'course_number':course_number,
        })

#Student join url creator:
def addEnrollmentForm(request, error_msg=''):
    return render(request, 'app/join.html', {'error':error_msg})

def handleEnrollmentForm(request,course_number,error_msg=''):
    #if request.method != "POST":
    #    return HttpResponse("Error: the request is not an HTTP POST request\n", status=500)
    #print(str(request.POST))
    return render(request,'app/join.html',{
        "course_name":Course.objects.get(course_number=course_number).course_name,
        "course_number":course_number,
    })

def handleFailureForm(request,course_number,error_msg=''):
    return render(request,'app/join_fail.html',{
        "course_name":Course.objects.get(course_number=course_number).course_name,
        "course_number":course_number,
        "error":error_msg,
    })

def enroll_success(request, course_number, error_msg=''):
    try:
        email = Student.objects.get(email=request.user.email)
        course = Course.objects.get(course_number=course_number)
    except:
        return addEnrollmentForm(request,error_msg = email + "is not a valid email")
    
    #check that student isn't already enrolled in a class at the specified time
    for already_enrolled in Enrollment.objects.filter(email=email):
        new_course_start = course.meet_start_time
        new_course_end = course.meet_end_time
        old_course = Course.objects.get(course_number=already_enrolled.course_number)
        old_start = old_course.meet_start_time
        old_end = old_course.meet_end_time
        if not ((new_course_start>old_end and new_course_end>old_end) or (new_course_start<old_start and new_course_end<old_start)):
            return addEnrollmentForm(request,error_msg= 'You are already enrolled in a class for that time slot')

    try:
        addEnrollment(email,course)
    except Exception as e:
        return handleFailureForm(request,course_number,error_msg='There is a database error in adding this student to course enrollment ' + str(e))
    return render(request,'app/join_success.html')

#Attendance:
def handleAttendanceForm(request,course_number,error_msg=''):
    try:
        teacher = Instructor.objects.get(email=request.user.email)
        if request.user.is_authenticated and Instructor.objects.filter(email=request.user.email).count()>0:
            if Course.objects.get(course_number=course_number,email=teacher.email) is not None:
                class_code = ''.join(random.choices(string.ascii_lowercase + string.digits, 10))
                generateQR(course_number,class_code)
                return render(request,'app/attendance_form.html',{
                    'error':error_msg,
                    'class_code':class_code,
                    'course_number':course_number,
                })
        else:
            return render(request,'course_created.html',{'error':'You are not the instructor for this course'})
    except:
        return render(request,'registration/login.html')
    
#uploading QR code:
def handleuploadQR(request,course_number,error_msg=''):
    #try:
    student = Student.objects.get(email=request.user.email)
    if request.user.is_authenticated and Student.objects.filter(email=request.user.email).count()>0:
        if Enrollment.objects.get(course_number=course_number,email=student.email) is not None:
            qr_id = Generate_QR.objects.get(qr_id=0)
            student_id = student
            uploadQR(qr_id,student_id)
            return render(request,'app/upload.html',{
                'error':error_msg,
                'course_number':course_number,
            })
        else:
            handleErrorForm(request,'You are not registered for this course!')
    else:
        handleErrorForm(request,'The authentification returned:' + str(request.user.is_authenticated) + 'the email count is'
                        + Student.objects.filter(email=request.user.email).count())
    #except:
    #    return render(request,'registration/login.html',{'error':'Please log in as a student'+str(var)})

def handleuploadQR(request,course_number,error_msg=''):
    return handleErrorForm(request,Generate_QR.objects.get(qr_id=0))

def handleErrorForm(request,error_msg=''):
    render(request,'app/error.html',{
        'error':error_msg,
    })
