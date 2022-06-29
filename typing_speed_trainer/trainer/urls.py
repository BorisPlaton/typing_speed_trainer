from django.urls import path
from trainer import views

app_name = 'trainer'

urlpatterns = [
    path('', views.TypingTrainer.as_view(), name='typing_trainer'),
    path('results/', views.ResultsList.as_view(), name='results'),
]
