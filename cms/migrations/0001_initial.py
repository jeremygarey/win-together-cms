# Generated by Django 4.1.5 on 2023-01-11 14:18

import ckeditor.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="BlogPost",
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
                ("name", models.CharField(max_length=200)),
                ("body", ckeditor.fields.RichTextField()),
                ("summary", models.CharField(max_length=1000)),
                ("main_image", models.CharField(max_length=300)),
                ("thumbnail_image", models.CharField(max_length=300)),
                ("added", models.DateTimeField(auto_now_add=True)),
                ("updated", models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name="TeamMember",
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
                ("name", models.CharField(max_length=200)),
                ("profile_image", models.CharField(max_length=300)),
                ("job_title", models.CharField(max_length=200)),
                ("email", models.CharField(max_length=200)),
                ("short_bio", models.CharField(max_length=1000)),
                ("long_bio", ckeditor.fields.RichTextField()),
            ],
        ),
    ]
