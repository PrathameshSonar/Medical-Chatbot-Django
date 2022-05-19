from django.urls import path
from . import views
from django.contrib.auth.views import LoginView

urlpatterns = [
    
    path('home', views.indexBMI,name='home'),
    
]