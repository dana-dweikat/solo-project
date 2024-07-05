# Generated by Django 5.0.6 on 2024-06-13 10:43

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("app1", "0002_remove_user_username"),
    ]

    operations = [
        migrations.AlterField(
            model_name="application",
            name="job",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="applications",
                to="app1.job",
            ),
        ),
    ]
