from django.urls import path
from . import views

urlpatterns = [
    path("set_profile",views.TestView.as_view())
]
