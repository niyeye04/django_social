from django.urls import path
from . import views
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('auth/', obtain_auth_token),
    path("register/",views.UserRegisteringView.as_view(),name = "user-register"),
    path("update_profile/",views.ProfileUpdateView.as_view(),name = "user-profile"), 
]
