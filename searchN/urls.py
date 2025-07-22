from django.urls import path
from . import views

urlpatterns = [
    path('function', views.hello_w), # function
    path('class', views.India.as_view()), # Class
    path('home', views.Home), # Home view
    path('search', views.search), 
]
