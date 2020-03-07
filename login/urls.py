from django.urls import path
from . import views

urlpatterns =[
	path("signup/", views.signup_view, name="signup_view"),
	path("home/", views.home_view, name="home_view"),
    path("login/",views.login_view,name="login_view"),
]