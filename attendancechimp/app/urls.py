from django.urls import path, include, re_path
#from django.conf.urls import url
from django.contrib import admin
from . import views
from django.views.generic.base import TemplateView

urlpatterns = [
    path('', views.index, name='index'),
    path('accounts/', include('django.contrib.auth.urls')),
#    path("new/", views.addUserForm, name='new'),
#    path('new/success/',views.success, name = 'success'),
    path("course/", views.handleCourseForm, name='course'),
    path("course/course_created/", views.course_created, name = 'course_created'),
    path('register/', views.handleUserForm, name = 'resgister'),
    path('login/', views.make_login, name='login'),
    path('logout/', views.logout_view,name='logout'),
    path('join/<int:course_number>',views.handleEnrollmentForm, name='join'),
    path('join/join_try/<int:course_number>',views.enroll_success, name='try join'),
    path('join/join_fail/<int:course_number>',views.handleFailureForm, name='join fail'),
    path('attendance/<int:course_number>',views.handleAttendanceForm, name='attendance'),
    path('upload/<int:course_number>',views.handleuploadQR,name='uploadQR'),
    path('error/',views.handleErrorForm,name='error'),

]
