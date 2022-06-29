from django.urls import path, include

from account import views
import django.contrib.auth.urls

app_name = 'account'

urlpatterns = [
    path('', views.Account.as_view(), name='profile'),
    path('auth/login/', views.UserLogin.as_view(), name='login'),
    path('auth/registration/', views.Registration.as_view(), name='registration'),
    path('auth/', include('django.contrib.auth.urls')),
]
