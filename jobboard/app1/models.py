from django.db import models
from django.contrib.auth.models import AbstractUser

from .choices import JobType

class User(AbstractUser):
    email = models.EmailField(unique=True)
    username = None
    favorite_jobs = models.ManyToManyField('app1.Job', related_name='favorite_jobs')

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["password"]


class Job(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posted_jobs")
    email = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    type = models.CharField(max_length=50, choices=JobType.choices)
    description = models.TextField()
    company_name = models.CharField(max_length=255)
    company_description = models.TextField(null=True, blank=True)
    logo = models.ImageField(upload_to="logo/")
    published_on = models.DateField(auto_now_add=True)


class Application(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="applied_jobs")
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name="applications")
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField()
    cover_letter = models.TextField()
    cv = models.FileField(upload_to="cvs/")
    published_on = models.DateField(auto_now_add=True)
