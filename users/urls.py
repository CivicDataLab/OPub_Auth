from django.urls import path

from . import views

urlpatterns = [
    path('check_user', views.check_user, name='check_user'),
    path('verify_token', views.verify_token, name='verify_token'),
    path('check_access', views.check_access, name='check_access')
]