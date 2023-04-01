from django.urls import path, include
from django.contrib import admin
from . import views
from django.views.generic.base import TemplateView

urlpatterns = [
    path('', views.index, name='index'),
    path('accounts/', include('django.contrib.auth.urls')),
    path("login", TemplateView.as_view(template_name='login.html'), name = 'login'),
]
