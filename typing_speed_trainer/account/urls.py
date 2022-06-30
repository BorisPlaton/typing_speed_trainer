from django.urls import path, include

from account import views

app_name = 'account'

urlpatterns = [
    path('<int:pk>/', views.Account.as_view(), name='profile'),
    path('auth/login/', views.UserLogin.as_view(), name='login'),
    path('auth/registration/', views.Registration.as_view(), name='registration'),
    path('auth/', include('django.contrib.auth.urls')),
]
