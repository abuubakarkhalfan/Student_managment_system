from django.db import models
from django.contrib.auth.models import User


class Student(models.Model):
    GENDER_CHOICES = [
        ("Male", "Male"),
        ("Female", "Female"),
    ]

    # Connect student details to the user's account
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="student_profile",
        null=True,
        blank=True,
    )

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    registration_number = models.CharField(max_length=50, unique=True)
    email = models.EmailField(unique=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    date_of_birth = models.DateField()
    course = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20)
    date_registered = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Result(models.Model):
    SEMESTER_CHOICES = [
        ("Semester 1", "Semester 1"),
        ("Semester 2", "Semester 2"),
    ]

    student = models.ForeignKey(
        Student, on_delete=models.CASCADE, related_name="results"
    )
    subject_name = models.CharField(max_length=100)
    semester = models.CharField(max_length=20, choices=SEMESTER_CHOICES)
    academic_year = models.CharField(max_length=9)
    marks = models.DecimalField(max_digits=5, decimal_places=2)
    lecturer_comment = models.TextField(blank=True)

    class Meta:
        ordering = ["subject_name"]
        constraints = [
            models.UniqueConstraint(
                fields=[
                    "student",
                    "subject_name",
                    "semester",
                    "academic_year",
                ],
                name="unique_student_subject_semester_year",
            )
        ]

    def __str__(self):
        return f"{self.student} - {self.subject_name} - {self.academic_year}"
