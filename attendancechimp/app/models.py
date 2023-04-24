from django.db import models
import logging

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
    course_number = models.CharField(max_length=20)
    instructor_id = models.ForeignKey(Instructor, on_delete=models.CASCADE)
    start = models.DateTimeField()
    end = models.DateTimeField()
    meet_time = models.CharField(max_length=100)

# creates model that lists all student enrollments in all courses
class Enrollment(models.Model):
    enrollment_id = models.AutoField(primary_key=True)
    course_id = models.ForeignKey(Course, on_delete=models.CASCADE)
    student_id = models.ForeignKey(Student, on_delete=models.CASCADE)

# creates model of each QR code generated
class Generate_QR(models.Model):
    qr_id = models.AutoField(primary_key=True)
    course_id = models.ForeignKey(Course, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    # `auto_now_add=True` automatically set field's value to time it was uploaded
    pic = models.ImageField()

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

    logging.info('Added a new Instructor ' + str((fn, ln, email, pwd)))

# adds a student to the Student class
def addStudent(fn, ln, email, pwd):
    logging.info('Trying to add student' + str((fn, ln, email, pwd)))
    #Check that student does not already have an account
    if Student.objects.filter(email=email).count()>0:
        raise ValueError('Another Student with email ' + email + 'exists')
    new_student = Student(first_name = fn, last_name = ln, email = email, password = pwd)
    new_student.save()
    logging.info('Added a new Student ' + str((fn, ln, email, pwd)))

# adds a course to the course class
def addCourse(name,num,in_id,start,end,meet_time):
    logging.info('Trying to add course' + str((name,num,in_id,start,end,meet_time)))
    
    #checks that there is no identical course in the database
    if Course.objects.filter(num=num).count()>0:
        raise ValueError('Another Course with Number ' + num + ' already exists')

    #checks that the instructor is not teaching another course at the same time


    #checks that start date is before end date:
    if start>end:
        raise ValueError('Start is after the end date ')

    new_course = Course(course_id=id,course_name=name,course_number=num,Instructor_id=in_id,start=start,end=end,meet_time=meet_time)
    new_course.save()

    logging.info('Added a new Course ' + str((id,name,num,in_id,start,end,meet_time)))


