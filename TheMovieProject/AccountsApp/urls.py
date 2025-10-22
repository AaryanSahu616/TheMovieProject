from django.urls import path
from .views import *

urlpatterns = [
    path("api/register/", RegisterAPIView.as_view(), name="register"),
    path("api/login/", LoginAPIView.as_view(), name="login"),
    path("api/logout/", LogoutAPIView.as_view(), name="logout"),
    path("api/profile/", ProfileAPIView.as_view(), name="profile"),

    # Page Views
    path("register-page/", RegisterPageView.as_view(), name="register_page"),
    path("", CustomLoginView.as_view(), name="login_page"),
    path("profile-page/", ProfilePageView.as_view(), name="profile_page"),
]
