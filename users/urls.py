# from django.contrib import admin
from django.urls import path,include
from . import views
# from corposhare.views import *

urlpatterns = [
    path('login/',views.UserLoginView.as_view()),
    path('profiles/',views.ProfileView.as_view()),
    path('profile/<str:id>',views.ProfileDetailView.as_view()),
]
