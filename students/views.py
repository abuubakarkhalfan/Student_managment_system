from django.views.generic import TemplateView, FormView, CreateView
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import View

from .models import Student, Result
from .forms import StudentForm


class HomePageView(TemplateView):
    template_name = "home.html"


class AboutPageView(TemplateView):
    template_name = "about.html"


# CREATE ACCOUNT
class RegisterPageView(FormView):
    template_name = "register.html"
    form_class = UserCreationForm
    success_url = reverse_lazy("login")

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("student_dashboard")
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.save()

        messages.success(
            self.request,
            "Your account has been created successfully. Please log in.",
        )

        return super().form_valid(form)


# LOGIN
class LoginPageView(FormView):
    template_name = "login.html"
    form_class = AuthenticationForm

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("student_dashboard")
        return super().dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["request"] = self.request
        return kwargs

    def form_valid(self, form):
        login(self.request, form.get_user())

        messages.success(
            self.request,
            "Welcome! You have logged in successfully.",
        )

        return redirect("student_dashboard")


# STUDENT REGISTRATION
class StudentCreateView(LoginRequiredMixin, CreateView):
    model = Student
    form_class = StudentForm
    template_name = "student_form.html"
    success_url = reverse_lazy("student_dashboard")
    login_url = reverse_lazy("login")

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if Student.objects.filter(user=request.user).exists():
                return redirect("student_dashboard")

        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.user = self.request.user

        messages.success(
            self.request,
            "Your student registration has been completed successfully.",
        )

        return super().form_valid(form)


# STUDENT DASHBOARD
# STUDENT DASHBOARD
class StudentDashboardView(LoginRequiredMixin, TemplateView):
    template_name = "student_dashboard.html"
    login_url = reverse_lazy("login")

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if not Student.objects.filter(user=request.user).exists():
                return redirect("student_register")

        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        student = Student.objects.filter(user=self.request.user).first()

        context["student"] = student

        if student:
            context["results"] = Result.objects.filter(student=student).order_by(
                "subject_name"
            )
        else:
            context["results"] = Result.objects.none()

        return context


# LOGOUT
class LogoutPageView(LoginRequiredMixin, View):
    login_url = reverse_lazy("login")

    def post(self, request, *args, **kwargs):
        logout(request)
        messages.success(request, "You have logged out successfully.")
        return redirect("login")
