from django.urls import path

from app import views
from rest_framework import routers

from app.views import UserAPI

urlpatterns = [
    path(r'user/', UserAPI.as_view())
]
