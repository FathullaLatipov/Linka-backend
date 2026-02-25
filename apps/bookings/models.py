from django.db import models

from apps.student_profiles.models import StudentProfile
from apps.lessons.models import Lessons
from apps.tutors_profiles.models import TutorsTimeTable


class Bookings(models.Model):
    status_type = (
        ("Pending", "Pending"),
        ("Accepted", "Accepted"),
        ("Canceled", "Canceled")
    )
    student = models.OneToOneField(StudentProfile, on_delete=models.CASCADE, related_name="student_bookings")
    tutor = models.ForeignKey(TutorsTimeTable, on_delete=models.CASCADE, related_name="tutor_bookings")
    lesson = models.ForeignKey(Lessons, on_delete=models.CASCADE, name="lesson")
    status = models.CharField(choices=status_type, null=False, default="Pending")
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f"{self.student.first_name} {self.student.last_name}  {self.comment}"


    class Meta:
        db_table = "bookings"
        verbose_name = "Booking"
        verbose_name_plural = "Bookings"