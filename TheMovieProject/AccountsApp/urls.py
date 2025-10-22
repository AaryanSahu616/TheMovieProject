from django.urls import path
from .views import *
from django.views.generic import TemplateView


urlpatterns = [
    path("api/register/", RegisterAPIView.as_view(), name="register"),
    path("api/login/", LoginAPIView.as_view(), name="login"),
    path("api/logout/", LogoutAPIView.as_view(), name="logout"),
    path("api/profile/", ProfileAPIView.as_view(), name="profile"),
    path("register-page/", TemplateView.as_view(template_name="accounts/register.html"), name="register_page"),
    path("login-page/", TemplateView.as_view(template_name="accounts/login.html"), name="login_page"),
    path("profile-page/", TemplateView.as_view(template_name="accounts/profile.html"), name="profile_page"),
]
