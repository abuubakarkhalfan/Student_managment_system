from django import forms
from .models import Student


class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = [
            "first_name",
            "last_name",
            "registration_number",
            "email",
            "gender",
            "date_of_birth",
            "course",
            "phone_number",
        ]

        widgets = {
            "date_of_birth": forms.DateInput(attrs={"type": "date"}),
        }
