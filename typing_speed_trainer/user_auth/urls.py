from django.contrib.auth.views import LogoutView
from django.urls import path

from user_auth import views


app_name = 'user_auth'

urlpatterns = [
    path('login/', views.UserLogin.as_view(), name='login'),
    path('registration/', views.Registration.as_view(), name='registration'),

    path('reset_password/', views.UserPasswordReset.as_view(), name='reset_password'),
    path('reset/<uidb64>/<token>/', views.UserPasswordResetConfirm.as_view(), name='password_reset_confirm'),
    path('logout/', LogoutView.as_view(), name='logout')
]
