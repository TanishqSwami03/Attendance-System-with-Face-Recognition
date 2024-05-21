from datetime import datetime, date
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import View
import face_recognition
from django.conf import settings
from .models import *
from django.db.models import Q
from .forms import *
from django.db import IntegrityError
from django.utils import timezone
from PIL import Image
import os
import cv2
import numpy as np

# Create your views here.


# @login_required
def home(request):
    return render(request, 'home.html', {})


def findEncodings(images):
    encodeList = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encoded_face = face_recognition.face_encodings(img)[0]
        encodeList.append(encoded_face)
    return encodeList

# def mark_attendance(request):
#     images_path = "media/student_images"
#     images = []
#     classNames = []
#     mylist = os.listdir(images_path)
#     for img_name in mylist:
#         img_path = os.path.join(images_path, img_name)
#         curImg = cv2.imread(img_path)
#         images.append(curImg)
#         classNames.append(os.path.splitext(img_name)[0])

#     encoded_face_train = findEncodings(images)

#     cap = cv2.VideoCapture(0)
#     attendance_marked = False  # Flag to track if attendance has been marked
#     while True:
#         success, img = cap.read()
#         imgS = cv2.resize(img, (0,0), None, 0.25,0.25)
#         imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)
#         faces_in_frame = face_recognition.face_locations(imgS)
#         encoded_faces = face_recognition.face_encodings(imgS, faces_in_frame)
#         for encode_face, faceloc in zip(encoded_faces,faces_in_frame):
#             matches = face_recognition.compare_faces(encoded_face_train, encode_face)
#             faceDist = face_recognition.face_distance(encoded_face_train, encode_face)
#             matchIndex = np.argmin(faceDist)
#             if matches[matchIndex]:
#                 name = classNames[matchIndex].upper().lower()
#                 print(name)
#                 try:
#                     student = Student.objects.get(name__iexact=name)
#                     # Check if attendance has already been marked for this student today
#                     if not Attendance.objects.filter(student=student, date=timezone.now().date()).exists() and not attendance_marked:
#                         attendance = Attendance(student=student, attendee_type='STUDENT')
#                         attendance.save()
#                         print(f"Attendance marked for {name}")
#                         attendance_marked = True  # Set flag to True after marking attendance
#                         messages.success(request, f"Attendance marked for {name}")
#                         break  # Break out of the loop after marking attendance
#                     else:
#                         print(f"Attendance already marked for {name} today")
#                 except Student.DoesNotExist:
#                     print(f"Student with name '{name}' does not exist.")

#         if attendance_marked:
#             break  # Break out of the loop if attendance is marked

#         cv2.imshow('webcam', img)
#         if cv2.waitKey(1) & 0xFF == ord('q'):
#             break

#     cap.release()
#     cv2.destroyAllWindows()
#     return render(request, 'home.html')

def mark_attendance(request):
    images_path = "media/student_images"
    images = []
    classNames = []
    mylist = os.listdir(images_path)
    for img_name in mylist:
        img_path = os.path.join(images_path, img_name)
        curImg = cv2.imread(img_path)
        images.append(curImg)
        classNames.append(os.path.splitext(img_name)[0])

    encoded_face_train = findEncodings(images)

    cap = cv2.VideoCapture(0)
    attendance_marked = False  # Flag to track if attendance has been marked
    while True:
        success, img = cap.read()
        imgS = cv2.resize(img, (0,0), None, 0.25,0.25)
        imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)
        faces_in_frame = face_recognition.face_locations(imgS)
        encoded_faces = face_recognition.face_encodings(imgS, faces_in_frame)
        for encode_face, faceloc in zip(encoded_faces,faces_in_frame):
            matches = face_recognition.compare_faces(encoded_face_train, encode_face)
            faceDist = face_recognition.face_distance(encoded_face_train, encode_face)
            matchIndex = np.argmin(faceDist)
            if matches[matchIndex]:
                name = classNames[matchIndex].upper().lower()
                print(name)
                try:
                    student = Student.objects.get(name__iexact=name)
                    # Get today's date
                    today = date.today()
                    # Check if attendance has already been marked for this student today
                    if not Attendance.objects.filter(student=student, date=today).exists() and not attendance_marked:
                        attendance = Attendance(student=student, attendee_type='STUDENT', time=datetime.now().time())
                        attendance.save()
                        print(f"Attendance marked for {name}")
                        attendance_marked = True  # Set flag to True after marking attendance
                        messages.success(request, f"Attendance marked for {name} !")
                    else:
                        messages.success(request, f"Attendance for {name} already marked !")
                        print(f"Attendance already marked for {name} today")
                    
                    # Close the camera and return to home page if attendance is marked
                    cap.release()
                    cv2.destroyAllWindows()
                    return render(request, 'home.html')
                        
                except Student.DoesNotExist:
                    print(f"Student with name '{name}' does not exist.")

        cv2.imshow('webcam', img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    return render(request, 'home.html')
def process_facial_image(facial_image):
    """
    Processes a facial image and returns the facial encoding.

    Args:
        facial_image: A NumPy array representing the facial image data.

    Returns:
        A NumPy array representing the facial encoding, or None if no face is detected.
    """
    try:
      # Extract facial encoding (assuming single face)
        encoding = face_recognition.face_encodings(facial_image)[0]
    except Exception as e:
        print(f"Error extracting encoding: {e}")
        return None

    return encoding

def admin_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username = username, password = password)
        if user is not None:
            if user.is_superuser:
                login(request, user)
                return redirect('admin-home')
            else:
                messages.error(request, "you do not have permission to access this page.")
        else:
            messages.error(request, "Invalid username or password.")
            return redirect('admin-login')
    return render(request, 'admin_login.html', {})

@login_required()
def admin_home(request):
    return render(request, 'admin_home.html', {})

@login_required()
def admin_logout(request):
    logout(request)
    return redirect('home')


def courses(request):
    courses = Course.objects.all()

    context = {'courses': courses}
    return render(request, 'courses.html', context)


def admin_new(request):
    form = AdminForm()
    if request.method == 'POST':
        if request.user.is_superuser:
            form = AdminForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'Admin created successfully.')
                return redirect('admin-home')
            else:
                messages.error(request, 'Form is not valid. Please correct the errors.')
        else:
            messages.error(request, 'You do not have permission to perform this action.')
    return render(request, 'admin_new.html', {'form': form})

def check_attendance(request):
    # Retrieve all attendance records ordered by time in descending order
    attendance_records = Attendance.objects.all().order_by('-time')

    # Create a list to store attendance details
    attendance_details = []

    # Iterate over each attendance record
    for attendance in attendance_records:
        # Check if the attendee is a student
        if attendance.attendee_type == 'STUDENT':
            # Get the associated student details
            student = attendance.student
            student_name = student.name
            student_section = student.section
            student_course = student.course.name
        else:
            # If the attendee is not a student, set details to None
            student_name = student_section = student_course = None

        # Add attendance details to the list
        attendance_details.append({
            'date': attendance.date,
            'time': attendance.time,
            'student_name': student_name,
            'student_section': student_section,
            'student_course': student_course,
        })

    # Pass the attendance details to the template
    return render(request, 'check_attendance.html', {'attendance_details': attendance_details})

def check_students(request):
    students = Student.objects.all()
    context = {'students': students}
    return render(request, 'check_students.html', context)


def add_students(request):
    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            student = form.save()  # Save student details and image
            image = request.FILES.get('image', None)  # Access uploaded image

            if image:
                # Process image and generate encoding
                image_array = face_recognition.load_image_file(image)
                print(type(image_array)) 
                encoding = process_facial_image(image_array)  # Call your processing function

                # Set user_type based on your logic (assuming 'STUDENT' for students)
                user_type = 'STUDENT'

                # Save encoding linked to student
                known_encoding = Known_Encoding(
                    user_type=user_type, student=student, encoding=encoding)
                known_encoding.save()

                messages.success(request, 'Student added successfully with facial encoding.')
            else:
                messages.warning(request, 'Student added, but no image was uploaded.')

            return redirect('home')  # Redirect to success page
    else:
        form = StudentRegistrationForm()
    return render(request, 'add_students.html', {'form': form})