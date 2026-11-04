from django.contrib import admin
from .models import Student, Result


@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    list_display = (
        "student",
        "subject_name",
        "semester",
        "academic_year",
        "marks",
    )

    list_filter = (
        "semester",
        "academic_year",
        "subject_name",
    )

    search_fields = (
        "student__first_name",
        "student__last_name",
        "student__registration_number",
        "subject_name",
    )

    ordering = ("student", "subject_name")


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = (
        "first_name",
        "last_name",
        "registration_number",
        "email",
        "course",
    )

    search_fields = (
        "first_name",
        "last_name",
        "registration_number",
    )
