from django.db import models

from apps.lessons.models import Lessons
from apps.tutors_profiles.models import TutorsTimeTable


class Bookings(models.Model):
    status_type = (
        ("Pending", "Pending"),
        ("Accepted", "Accepted"),
        ("Canceled", "Canceled")
    )
    comment = models.TextField()
    lesson = models.ForeignKey(Lessons, on_delete=models.CASCADE, name="lesson")
    user = models.IntegerField()
    tutor = models.ForeignKey(TutorsTimeTable, on_delete=models.CASCADE, related_name="bookings")
    status = models.CharField(choices=status_type, null=False, default="Pending")
    created_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f"{self.user}  {self.comment}"


    class Meta:
        db_table = "bookings"