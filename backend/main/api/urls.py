from django.urls import path
from . import views

urlpatterns = [
    path("set_profile/",views.TestView.as_view()),
    path("register/",views.UserRegisteringView.as_view(),name = "user-register"),
    
]
