from django.urls import path

from account import views

app_name = 'account'

urlpatterns = [
    path('<int:pk>/', views.Account.as_view(), name='profile'),
    path('delete/photo/<int:pk>/', views.DeleteProfilePhoto.as_view(), name='delete_profile_photo'),
]
