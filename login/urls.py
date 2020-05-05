from django.urls import path
from django.conf.urls import url
from . import views

urlpatterns =[
	path("signup/", views.signup_view, name="signup_view"),
	path("home/", views.home_view, name="home_view"),
	url(r'^home/(?P<pk>[0-9]+)/$', views.home_view, name="home_view_with_pk"),
    path("login/",views.login_view,name="login_view"),
	path("logout/",views.logout_view,name="logout_view"),
	path("driver/",views.auto_view,name="auto_view"),
	url(r'^driver/(?P<pk>[0-9]+)/$', views.auto_view, name="auto_view_with_pk"),
]
