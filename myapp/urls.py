from django.urls import path
from . import views

urlpatterns = [
    path('call-grpc/', views.call_grpc, name='call_grpc'),
    path('create-user/', views.create_user, name='create_user'),
]
