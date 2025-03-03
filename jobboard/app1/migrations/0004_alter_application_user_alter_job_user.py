# Generated by Django 5.0.6 on 2024-06-13 17:54

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("app1", "0003_alter_application_job"),
    ]

    operations = [
        migrations.AlterField(
            model_name="application",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="applied_jobs",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AlterField(
            model_name="job",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="posted_jobs",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
