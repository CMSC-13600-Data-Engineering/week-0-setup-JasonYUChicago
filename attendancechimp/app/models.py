from django.db import models
import logging
from django.contrib.auth.models import User

logging.basicConfig(level=logging.DEBUG)


# Create your models here.
# creates model that lists each student
class Student(models.Model):
    student_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=50, null=False)
    last_name = models.CharField(max_length=50, null=False)
    email = models.EmailField(unique=True, null=False)
    password = models.CharField(max_length=100, null=False)

# creates model that lists each instructor
class Instructor(models.Model):
    instructor_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=50, null=False)
    last_name = models.CharField(max_length=50, null=False)
    email = models.EmailField(unique=True, null=False)
    password = models.CharField(max_length=100, null=False)

# creates model that lists each course
class Course(models.Model):
    course_id = models.AutoField(primary_key=True)
    course_name = models.CharField(max_length=100)
    course_number = models.CharField(unique=True, null=False, max_length=20)
    instructor_id = models.ForeignKey(Instructor, on_delete=models.CASCADE)
    start = models.DateTimeField(null=False)
    end = models.DateTimeField(null=False)
    meet_days = models.CharField(max_length=100, null=False)
    meet_start_time = models.CharField(max_length=100, null=False)
    meet_end_time = models.CharField(max_length=100, null=False)


# creates model that lists all student enrollments in all courses
class Enrollment(models.Model):
    enrollment_id = models.AutoField(primary_key=True)
    course_number = models.ForeignKey(Course, null=True, to_field='course_number', on_delete=models.CASCADE)
    email = models.ForeignKey(Student, null=True, to_field='email', on_delete=models.CASCADE)

# creates model of each QR code generated
class Generate_QR(models.Model):
    qr_id = models.AutoField(primary_key=True)
    course_number = models.ForeignKey(Course, to_field='course_number', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    # `auto_now_add=True` automatically set field's value to time it was uploaded
    class_code = models.CharField(max_length=11,null=False)

# creates a model that keeps track of QRs uploaded
class Upload_QR(models.Model):
    upload_id = models.AutoField(primary_key=True)
    qr_id = models.ForeignKey(Generate_QR, on_delete=models.CASCADE)
    student_id = models.ForeignKey(Student, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

# adds an instructor to the Instructor class
def addInstructor(fn, ln, email, pwd):
    logging.info('Trying to add instructor'+ str((fn, ln, email, pwd)))

    if Instructor.objects.filter(email=email).count()>0:
        raise ValueError('Another Instructor with Email ' + email + 'exists')

    new_instructor = Instructor(first_name = fn, last_name = ln, email = email, password = pwd)
    new_instructor.save()
    
    user = User.objects.create_user(username=email,password=pwd, email=email, first_name=fn, last_name=ln)
    user.save()

    logging.info('Added a new Instructor ' + str((fn, ln, email, pwd)))

# adds a student to the Student class
def addStudent(fn, ln, email, pwd):
    logging.info('Trying to add student' + str((fn, ln, email, pwd)))
    #Check that student does not already have an account
    if Student.objects.filter(email=email).count()>0:
        raise ValueError('Another Student with email ' + email + 'exists')
    new_student = Student(first_name = fn, last_name = ln, email = email, password = pwd)
    new_student.save()

    user = User.objects.create_user(username=email,password=pwd, email=email, first_name=fn, last_name=ln)
    user.save()

    logging.info('Added a new Student ' + str((fn, ln, email, pwd)))

# adds a course to the course class

def addCourse(name,num,in_id,start,end,meet_days,meet_start_time,meet_end_time):
    logging.info('Trying to add course' + str((name,num,in_id,start,end,meet_days,meet_start_time,meet_end_time)))
    
    #checks that there is no identical course in the database
    if Course.objects.filter(course_number=num).count()>0:
        raise ValueError('Another Course with Number ' + num + ' already exists')
    
    new_course = Course(course_name=name, course_number=num, instructor_id=in_id, 
                        start=start, end=end, meet_days=meet_days, 
                        meet_start_time=meet_start_time, meet_end_time=meet_end_time)
    new_course.save()
    
    logging.info('Added course ' + str(new_course))

def addEnrollment(email, num):
    logging.info('Trying to add student' + str(email) + 'to course' +str(num))
    if Enrollment.objects.filter(course_number=num,email=email).count()>0:
        raise ValueError('You have already enrolled in this course')
    new_enrollment = Enrollment(course_number=num,email=email)
    new_enrollment.save()
    logging.info('Added student' + str(email) + 'to course' +str(num))

def generateQR(course_number,class_code):
    if generateQR.objects.filter(class_code=class_code).count()>0:
        raise ValueError('This class already has a class code associated with it')
    newQR = Generate_QR(course_number=course_number, class_code=class_code)
    newQR.save()

def uploadQR(qr_id,student_id):
    newQR = Upload_QR(qr_id=qr_id,student_id=student_id)
    newQR.save()
    
