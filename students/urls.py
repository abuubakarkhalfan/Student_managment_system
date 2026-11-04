from django.urls import path

from .views import (
    HomePageView,
    AboutPageView,
    RegisterPageView,
    LoginPageView,
    StudentCreateView,
    StudentDashboardView,
    LogoutPageView,
)

urlpatterns = [
    path("", HomePageView.as_view(), name="home"),

    path("about/", AboutPageView.as_view(), name="about"),

    path("register/", RegisterPageView.as_view(), name="register"),

    path("login/", LoginPageView.as_view(), name="login"),

    path(
        "student/register/",
        StudentCreateView.as_view(),
        name="student_register",
    ),

    path(
        "dashboard/",
        StudentDashboardView.as_view(),
        name="student_dashboard",
    ),

    path(
        "logout/",
        LogoutPageView.as_view(),
        name="logout",
    ),
]