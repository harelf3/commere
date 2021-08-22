from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("listing/<str:name>", views.active_listing,name="active_listing"),
    path("create",views.create,name="create")
    #dont forgt to send name as a parameter
]
