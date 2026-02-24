from django.db import models
from apps.users.models import User

class TutorsProfile(models.Model):
    first_name = models.CharField(null=False,blank=False)
    last_name = models.CharField(null=False, blank=False)
    profile_image = models.FileField(upload_to="profile_images/")
    certificate_image = models.FileField(upload_to="certifications/")
    ielts_score = models.FloatField(null=False, blank=False)
    experience = models.IntegerField(null=False, blank=False)
    is_deleted = models.BooleanField(null=False, blank=False,default=False)
    user = models.OneToOneField(User,on_delete=models.CASCADE, related_name="tutor_profile")
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        db_table = 'tutors_profile'


class TutorsTimeTable(models.Model):
    tutor = models.ForeignKey(TutorsProfile, on_delete=models.CASCADE, related_name="tutors_time_table")
    day_of_week = models.IntegerField(null=False, blank=False)
    available_time = models.TimeField(null=False, blank=False)
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.tutor.first_name} {self.tutor.last_name}"