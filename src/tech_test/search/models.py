from django.db import models

# Create your models here.

class Job(models.Model):
    _id = models.CharField(max_length=20)
    objective = models.CharField(max_length=200, default = "")
    type = models.CharField(max_length=200, default = "")
    organization_name = models.CharField(max_length=200)
    organization_picture = models.URLField(default = "")
    locations = models.CharField(max_length=200, default = "")
    remote = models.BooleanField(default = False)
    skills = models.CharField(max_length=200, default = "")
    compensation = models.CharField(max_length=200, default = "")
    def __str__(self):
        return f'{self.id} {self.objective}'