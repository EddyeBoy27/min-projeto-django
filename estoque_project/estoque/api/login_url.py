from django.urls import path
from django.contrib.auth import views

# from .. import views

app_name = "login"

urlpatterns = [
    # path("", views.LoginView.as_view(), name="login"),
    path("login/", views.auth_login, {'template_name': 'login.html'}, name="login")
]
