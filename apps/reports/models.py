from django.db import models

class Reports(models.Model):
    comment = models.TextField(null=False, blank=False)
    user = models.IntegerField(null=False, blank=False)
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.comment

    class Meta:
        db_table = "reports"