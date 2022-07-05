from django.urls import path

from account import views

app_name = 'account'

urlpatterns = [
    path('<int:pk>/', views.Account.as_view(), name='profile'),
    path('delete/photo/', views.DeleteProfilePhoto.as_view(), name='delete_profile_photo'),
    path('update/photo/', views.UpdateProfilePhoto.as_view(), name='update_profile_photo'),
    path('update/settings/', views.UpdateProfileSettings.as_view(), name='update_profile_settings'),
]
