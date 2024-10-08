""" Initial migrations

Generated by Django 3.2 on 2021-10-01.
"""

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):
    """Migration"""

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Instance",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        max_length=200,
                        unique=True,
                        validators=[
                            django.core.validators.RegexValidator(
                                code="invalid_title",
                                message="Title must not be empty or only whitespaces",
                                regex=".*\\S.*",
                            )
                        ],
                    ),
                ),
                ("endpoint", models.URLField(unique=True)),
                ("access_token", models.CharField(max_length=200)),
                ("refresh_token", models.CharField(max_length=200)),
                ("expires", models.DateTimeField()),
            ],
        ),
    ]
