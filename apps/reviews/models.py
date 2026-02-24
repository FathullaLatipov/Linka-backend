from django.db import models

from apps.student_profiles.models import StudentProfile
from apps.tutors_profiles.models import TutorsProfile


class Reviews(models.Model):
    tutor = models.ForeignKey(TutorsProfile,on_delete=models.CASCADE,related_name="tutor_reviews")
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name="reviews")
    comment = models.TextField(null=False, blank=False)
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.tutor.first_name


    class Meta:
        db_table = "comments"
