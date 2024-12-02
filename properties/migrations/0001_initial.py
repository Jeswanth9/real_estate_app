# Generated by Django 5.0.4 on 2024-11-19 20:07

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Property",
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
                ("title", models.CharField(max_length=200, unique=True)),
                ("description", models.TextField(blank=True)),
                ("location", models.CharField(max_length=255)),
                (
                    "property_type",
                    models.CharField(
                        choices=[
                            ("apartment", "Apartment"),
                            ("house", "House"),
                            ("land", "Land"),
                            ("commercial", "Commercial"),
                        ],
                        max_length=50,
                    ),
                ),
                ("price", models.DecimalField(decimal_places=2, max_digits=10)),
                (
                    "area",
                    models.DecimalField(
                        decimal_places=2,
                        help_text="Area in square meters",
                        max_digits=7,
                    ),
                ),
                ("images", models.ImageField(blank=True, upload_to="property_images/")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "owner",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="properties",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "ordering": ["-created_at"],
            },
        ),
    ]