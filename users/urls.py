from django.urls import path, include
from .views import DashboardView, RegisterView
from .tokens import activate

urlpatterns = [
    path("dashboard/", DashboardView.as_view(), name="dashboard"),
    path("accounts/", include("django.contrib.auth.urls")),
    path("oauth/", include("social_django.urls")),
    path("register/", RegisterView.as_view(), name="register"),
    path("activate/<uidb64>/<token>", activate, name="activate")
]