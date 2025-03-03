# Generated by Django 5.0.6 on 2024-06-14 08:07

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("app1", "0005_alter_job_type"),
    ]

    operations = [
        migrations.AddField(
            model_name="application",
            name="published_on",
            field=models.DateField(
                auto_now_add=True, default=django.utils.timezone.now
            ),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="job",
            name="published_on",
            field=models.DateField(
                auto_now_add=True, default=django.utils.timezone.now
            ),
            preserve_default=False,
        ),
    ]
