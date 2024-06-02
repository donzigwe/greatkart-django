from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('register', views.register, name="register"),
    path('login', views.login, name="login"),
    path('logout', views.logout, name="logout"),
    path('verification/<email>/', views.verification_sent, name='verification_sent'),
    path('dashboard', views.dashboard, name="dashboard"),
    path('', views.dashboard, name="dashboard"),

    path('forgot_password', views.forgot_password, name="forgot_password"),
    path('activate/<uidb64>/<token>/', views.activate, name="activate"),
    path('reset_password_validation/<uidb64>/<token>/', views.reset_password_validation, name="reset_password_validation"),
    path('reset_password', views.reset_password, name="reset_password"),
    path('change_password', views.change_password, name="change_password"),
]
