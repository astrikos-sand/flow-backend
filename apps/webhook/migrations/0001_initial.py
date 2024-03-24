# Generated by Django 5.0.2 on 2024-03-16 08:08

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("flow", "0003_slot_speciality"),
    ]

    operations = [
        migrations.CreateModel(
            name="WebHookEvent",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("name", models.CharField(blank=True, max_length=255, null=True)),
                ("description", models.TextField(blank=True, null=True)),
                (
                    "trigger_node",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="flow.genericnode",
                    ),
                ),
            ],
            options={
                "ordering": ("-created_at", "-updated_at"),
                "abstract": False,
            },
        ),
    ]