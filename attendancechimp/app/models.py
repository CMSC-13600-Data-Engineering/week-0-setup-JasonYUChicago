from django.db import models

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
