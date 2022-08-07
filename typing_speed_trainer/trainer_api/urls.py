from django.urls import path
from rest_framework.routers import SimpleRouter

from trainer_api import views


app_name = 'trainer_api'

router = SimpleRouter()
router.register('result', views.ResultsList, basename='result')

urlpatterns = [
    path('result/template/', views.result_template, name='result_template'),
    *router.urls,
]
