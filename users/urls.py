from django.urls import path

from . import views

urlpatterns = [
    path('register', views.register, name='register'),
    path('verify_token', views.verify_token, name='verify_token')
]