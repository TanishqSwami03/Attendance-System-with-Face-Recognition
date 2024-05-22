from django.contrib.auth.models import AbstractUser
import base64
from django.db import models

# Create your models here.
    
class Course(models.Model):
    name = models.CharField(max_length=100, unique = True)

    def __str__(self):
        return self.name
    
class Department(models.Model):
    name = models.CharField(max_length=100, unique = True)

    def __str__(self):
        return self.name
    
class Designation(models.Model):
    name = models.CharField(max_length=100, unique = True)

    def __str__(self):
        return self.name

class Faculty(models.Model):
    name = models.CharField(max_length=100)
    department = models.ForeignKey(Department, on_delete = models.CASCADE)
    designation = models.ForeignKey(Designation, on_delete = models.CASCADE)

    def __str__(self):
        # return self.name
        return self.name + ' - ' + self.designation.name


class Student(models.Model):
    name = models.CharField(max_length=100)
    section = models.CharField(max_length=100)
    course = models.ForeignKey(Course, on_delete = models.CASCADE)
    image = models.FileField(upload_to='student_images/', blank=True, null=True)

    def __str__(self):
        return self.name + ' - ' + self.course.name
        
class Known_Encoding(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, null=True, blank=True)  # Optional for Student
    encoding = models.BinaryField(max_length=1024)

    def __str__(self):
        if self.student:
            return f"Student - {self.student.id} Encoding"
        else:
            return "Unknown User Encoding"  # Handle cases where neither is assigned
 
    def get_encoding_as_b64(self):
        return base64.b64encode(self.encoding).decode("utf-8")
    
    def set_encoding_as_b64(self, b64_encoding):
        self.encoding = base64.b64decode(b64_encoding)
    

class Attendance(models.Model):
    date = models.DateField(auto_now_add=True)  # Automatically set on object creation
    time = models.TimeField(auto_now=True) # Automatically set on object creation
    # Person who attended (either Student or Faculty)
    # attendee_type = models.CharField(max_length=20, choices=(('STUDENT', 'Student'), ('FACULTY', 'Faculty')))
    student = models.ForeignKey(Student, on_delete=models.CASCADE, null=True, blank=True)  # Optional for Student
    # faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE, null=True, blank=True)  # Optional for Faculty

    def __str__(self):
        if self.student:
            return f"{self.student.name} - {self.date}"
        else:
            return f"Unknown Attendee - {self.date}"