from django.db import models


# Create your models here.
class LossPreventionPattern(models.Model):
    description = models.CharField(max_length=255, null=True, blank=True)
    pattern = models.TextField()

    def __str__(self):
        return self.description


class DataLeak(models.Model):
    message = models.TextField()
    content = models.TextField(null=True, blank=True)
    channel = models.CharField(max_length=255)
    pattern = models.ForeignKey(LossPreventionPattern, on_delete=models.CASCADE)

    def __str__(self):
        return self.message
