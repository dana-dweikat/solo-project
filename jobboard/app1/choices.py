from django.db import models


class JobType(models.TextChoices):
    PART_TIME = "part_time", "Part Time"
    FULL_TIME = "full_time", "Full Time"