from django.urls import path

from . import views

urlpatterns = [
    path('verify_user_token', views.verify_user_token, name='verify_user_token'),
    path('check_user', views.check_user, name='check_user'),
    path('check_user_access', views.check_user_access, name='check_user_access'),
    path('create_user_role', views.create_user_role, name='create_user_role'),
    path('get_users', views.get_users, name='get_users')
]