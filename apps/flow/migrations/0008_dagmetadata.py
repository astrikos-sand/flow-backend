# Generated by Django 5.0.2 on 2024-12-16 07:16

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("flow", "0007_functiondatastore"),
    ]

    operations = [
        migrations.CreateModel(
            name="DAGMetaData",
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
                ("created_at", models.DateTimeField(auto_now_add=True, null=True)),
                ("updated_at", models.DateTimeField(auto_now=True, null=True)),
                ("config", models.JSONField(default=dict)),
                (
                    "flow",
                    models.OneToOneField(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="flow.flow",
                    ),
                ),
            ],
            options={
                "ordering": ("-created_at", "-updated_at"),
                "abstract": False,
            },
        ),
    ]