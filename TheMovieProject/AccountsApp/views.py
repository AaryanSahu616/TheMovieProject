from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .models import User
from .serializers import UserSerializer
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.contrib.auth import get_user_model
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy


class RegisterAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        username = request.data.get("username")
        email = request.data.get("email")
        password = request.data.get("password")


        if not username or not password:
            return Response({"error": "Username and password are required"}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create(
            username=username,
            email=email,
            role=User.ROLE_CHOICES[1][0],  # default to 'user'
            # bio=bio,
            # profile_pic=profile_pic,
            password=make_password(password)  # hash password
        )
        login(request, user)
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class LoginAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            serializer = UserSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

class LogoutAPIView(APIView):
    def post(self, request):
        logout(request)
        return Response({"message": "Logged out successfully"})

class ProfileAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

class CustomLoginView(LoginView):
    template_name = "accounts/login.html"

    def dispatch(self, request, *args, **kwargs):
        # If already logged in, redirect to /movies/
        if request.user.is_authenticated:
            return redirect(reverse_lazy("movie_list_template"))
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy("movie_list_template")

class RegisterPageView(TemplateView):
    template_name = "accounts/register.html"

    def dispatch(self, request, *args, **kwargs):
        # If user is already logged in, redirect to movies
        if request.user.is_authenticated:
            return redirect("movie_list_template")
        return super().dispatch(request, *args, **kwargs)   

class ProfilePageView(LoginRequiredMixin, TemplateView):
    template_name = "accounts/profile.html"
    login_url = "/api/login/"  # redirect here if not logged in

    # Optional: you can override get_context_data if you need user info
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        return context

