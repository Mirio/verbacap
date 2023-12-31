# Generated by Django 4.2.6 on 2023-10-23 21:02

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0003_provider_shortname"),
    ]

    operations = [
        migrations.CreateModel(
            name="Settings",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_at", models.DateTimeField(db_index=True, default=django.utils.timezone.now)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("enabled", models.BooleanField(default=True)),
                ("name", models.CharField(help_text="Settings Name")),
                ("value", models.CharField(help_text="Value of the setting")),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
