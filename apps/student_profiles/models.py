from apps.users.models import User
from django.db import models


class StudentProfile(models.Model):
    type = (
        ("Male", "Male"),
        ("Female", "Female")
    )
    level_types = [
        ("beginner", "beginner"),
        ("elementary", "elementary"),
        ("pre-intermediate", "pre-intermediate"),
        ("intermediate", "intermediate"),
        ("upper-intermediate", "upper-intermediate"),
        ("advanced","advanced"),
        ("Ielts", "ielts")
    ]
    first_name = models.CharField(null=False, blank=False)
    last_name = models.CharField(null=False, blank=False)
    profile_image = models.FileField(upload_to="profile_images/")
    englishLevel = models.CharField(choices=level_types, null=False, blank=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="student_profile")
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        db_table = 'students_profile'
