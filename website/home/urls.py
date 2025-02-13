from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('trackers/', views.trackers, name='trackers'),
    path('reports/', views.reports, name='reports'),
]