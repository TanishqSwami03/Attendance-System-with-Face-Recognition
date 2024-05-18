from .models import *
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class AddCourse(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['name']


class AdminForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_staff = True
        user.is_superuser = True
        if commit:
            user.save()
        return user

class StudentRegistrationForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['name', 'section', 'course', 'image']
        widgets = {
            'image': forms.FileInput(attrs={'accept': 'image/*'}),  # Optional: Restrict file types
        }
