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
    path("course/", views.addCourseForm, name='course'),
    path("course/course_created/", views.course_created, name = 'course_created'),
    path('register/', views.handleUserForm, name = 'resgister'),
    path('login/', views.login, name='login'),

]
