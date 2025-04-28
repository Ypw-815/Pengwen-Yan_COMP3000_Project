from django.urls import path
from . import views
from .views import root_view
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', root_view, name='root'),
    path('login/', views.login_view, name='login'),
    path('user_login/', views.user_login, name='user_login'),
    path('user_register/', views.user_register, name='user_register'),

    path('user_logout', views.logout_view, name='user_logout'),
    path('profile/', views.profile, name='profile'),

    path('datafile/', views.datafile, name='datafile'),

    path('password_change/', auth_views.PasswordChangeView.as_view(), name='password_change'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),
]