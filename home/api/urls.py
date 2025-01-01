from django.contrib import admin
from django.urls import path
from home.views import LoginUser, RegisterUser, ProtectedApi

urlpatterns = [
    path('register/', RegisterUser.as_view()),
    path('login/', LoginUser.as_view()),
    path('protected/', ProtectedApi.as_view())
]
