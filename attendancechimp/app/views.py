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
    try:
        email = request.POST['email']
        password = request.POST['pwd']
        user = authenticate(username=email, password=password)
        if user is not None:
            login(request,user)
            return render(request, 'app/success.html')
        else:
            return loginForm(request, error_msg='did not work')
    except:
        return loginForm(request,'Please Enter a Valid Username and Password')

#Logout:
def logout_view(request):
    logout(request)
    return loginForm(request,'You have just logged out!')
    

#ADDING INSTRUCTORS & STUDENTS

def addUserForm(request, error_msg=''):
    return render(request, 'app/register.html', {'error':error_msg})

def handleUserForm(request):
    #if request.method != "POST":
    #    return HttpResponse("Error: the request is not an HTTP POST request\n", status=500)
    #print(str(request.POST))

    #Check what role the person signing in is (instructor or student)
    try:
        type = request.POST['role']
    except:
        return addUserForm(request,error_msg='Please designate if you are an Instructor or Student')

    #Assign needed variables from user input
    try:
        first_name = request.POST['fn']
        last_name = request.POST['ln']
        email = request.POST['email']
        password = request.POST['pwd']
    except:
        return addUserForm(request, error_msg='Please fill out all the fields of the form')
    
    #Try adding a user based on the indicated role (Instructor/Student)
    if(type=='Instructor'):
        try:
            addInstructor(first_name,last_name,email,password)
        except Exception as e:
            return addUserForm(request, error_msg='Error: There is a database error in adding this Instructor: ' + str(e))
    elif(type == 'Student'):
        try:
            addStudent(first_name,last_name,email,password)
        except Exception as e:
            return addUserForm(request,error_msg='Error: There is a database error in adding this Student: ' + str(e))
    
    #Log the user in after sign up
    return make_login(request)


#THE /app/create VIEW

def addCourseForm(request, error_msg=''):
    return render(request, 'app/course.html', {'error':error_msg})
    
def handleCourseForm(request):
    #if request.method != "POST":
    #    return HttpResponse("Error: the request is not an HTTP POST request\n", status=500)
    #print(str(request.POST)

    #Try to access user data to see if they are actually logged in
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
        return addCourseForm(request,error_msg='Please fill out all the fields of the form')
    
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
    
    #Tries to create a new entry in the Course table with the input data
    try:
        addCourse(course_name,course_number,Instructor_id,start,end,meet_days,meet_start,meet_end)
    except Exception as e:
        return addCourseForm(request, error_msg='Error: There is a database error in adding this Course ' + str(e))
    return course_created(request,course_number=course_number,course_name=course_name)

def course_created(request, error_msg='',course_number='',course_name=''):
    return render(request,'app/course_created.html',{
        'error':error_msg,
        'course_number':course_number,
        'course_name':course_name
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
        "error":error_msg,
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
        return handleEnrollmentForm(request,course_number=course_number,error_msg = request.user.email + " is not a valid Student email")

    #check that student is not already enrolled in a course happening at the same time
    for already_enrolled in Enrollment.objects.filter(email=email):
        new_course_start = course.meet_start_time
        new_course_end = course.meet_end_time
        old_course = Course.objects.get(course_number=already_enrolled.course_number.course_number)
        old_start = old_course.meet_start_time
        old_end = old_course.meet_end_time
        if not ((new_course_start>old_end and new_course_end>old_end) or (new_course_start<old_start and new_course_end<old_start)):
            return handleFailureForm(request,course_number=course_number,error_msg= 'You are already enrolled in a class for that time slot')

    #populate the Enrollment class with the current users information
    try:
        addEnrollment(email,course)
    except Exception as e:
        return handleFailureForm(request,course_number,error_msg='There is a database error in adding this student to course enrollment: ' + str(e))
    return render(request,'app/join_success.html')

#Attendance:
def handleAttendanceForm(request,course_number,error_msg=''):
    #checks that the user is logged in
    if request.user.is_authenticated:
        #checks that the user is an instructor:
        try:
            teacher = Instructor.objects.get(email=request.user.email)
        except:
            return loginForm(request,'Please log in as an Instructor to access course attendance')
        class_code = ''.join(random.choices(string.ascii_lowercase + string.digits,k=10))
        try:  
            course_num = Course.objects.get(course_number=course_number)
        except:
            return handleErrorForm(request,error_msg='No such course exists!')
        try:
            if Course.objects.get(course_number=course_number).instructor_id.instructor_id==teacher.instructor_id:
                generateQR(course_num,class_code)
                return render(request,'app/attendance_form.html',{
                    'error':error_msg,
                    'class_code':class_code,
                    'course_number':course_number,
                })
            else:
                return handleErrorForm(request,error_msg ='You are not the instructor for this course!')
        except:
            return handleErrorForm(request, error_msg='what is happening?')
    else:
        return loginForm(request,'Please log in before doing anything else!')

   
#uploading QR code:
def handleuploadQR(request,course_number,error_msg=''):
    #checks that current user is logged in
    if request.user.is_authenticated:
        #check that current user is a student
        try:
            student = Student.objects.get(email=request.user.email)
        except:
            return handleErrorForm(request,error_msg='You are not a student. Please login as a student.')
        try:  
            course_num = Course.objects.get(course_number=course_number)
        except:
            return handleErrorForm(request,error_msg='No such course exists!')
        try:
            img = request.POST['file']
        except:
            return render(request,'app/upload.html',{'error':'No file detected!'})
        try:
            if Enrollment.objects.filter(email=student.email).get(course_number=course_number) is not None:
                course_qrs = Generate_QR.objects.filter(course_number=course_number)
                class_code = course_qrs[len(course_qrs)-1].class_code
                student_id = student.student_id
                uploadQR(class_code =  class_code, student_id = student_id,img=img)
                return render(request,'app/upload.html',{
                    'error':error_msg,
                    'course_number':course_number,
                })
            else:
                handleErrorForm(request,'You are not registered for this course!')
        except:
            return handleErrorForm(request, 'Could not update your attendance!')
    else:
        return loginForm(request,'Please login first')


def handleErrorForm(request,error_msg=''):
    return render(request,'app/error.html',{
        'error':error_msg,
    })
