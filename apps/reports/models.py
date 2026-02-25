from django.db import models

from apps.student_profiles.models import StudentProfile


class Reports(models.Model):
    student = models.ForeignKey(StudentProfile,on_delete=models.CASCADE, related_name="reports")
    comment = models.TextField(null=False, blank=False)
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.student.first_name} {self.student.last_name}  {self.comment}"

    class Meta:
        db_table = "reports"
        verbose_name = "Report"
        verbose_name_plural = "Reports"