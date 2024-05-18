from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('admin-home/', views.admin_home, name='admin-home'),
    path('admin-new/', views.admin_new, name='admin-new'),
    path('admin-login/', views.admin_login, name='admin-login'),
    path('admin-logout/', views.admin_logout, name='admin-logout'),
    path('check-students/', views.check_students, name='check-students'),
    path('check-attendance/', views.check_attendance, name='check-attendance'),
    path('courses/', views.courses, name='courses'),
    path('add-students/', views.add_students, name='add-students'),
    path('mark-attendance/', views.mark_attendance, name='mark-attendance'),
]
