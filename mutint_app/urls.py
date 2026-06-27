from django.urls import path
from . import views

app_name = 'mutint_app'

urlpatterns = [
    path('', views.index, name='index'),
]
