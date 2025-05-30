from django.urls import path
from . import views

app_name = 'parking'

urlpatterns = [
    path('', views.parking_list, name='parking_list'),
    path('<int:pk>/', views.parking_detail, name='parking_detail'),
]
