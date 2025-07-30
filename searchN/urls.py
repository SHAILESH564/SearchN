from django.urls import path
from . import views

urlpatterns = [
    path('search/', views.search), 
    path('search/get-count', views.get_count, name='get_count'), # Get count of SearchN objects
]
