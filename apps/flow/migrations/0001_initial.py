# Generated by Django 5.0.2 on 2024-03-14 07:56

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="FlowFile",
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
                ("name", models.CharField(max_length=100)),
                ("description", models.TextField(blank=True, null=True)),
            ],
            options={
                "ordering": ("-created_at", "-updated_at"),
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="NodeClass",
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
                ("name", models.CharField(max_length=100, unique=True)),
                ("description", models.TextField(blank=True, null=True)),
                ("code", models.FileField(upload_to="flow/node_classes/")),
            ],
            options={
                "ordering": ("-created_at", "-updated_at"),
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Node",
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
                (
                    "flow_file",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="nodes",
                        to="flow.flowfile",
                    ),
                ),
                (
                    "node_class",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="nodes",
                        to="flow.nodeclass",
                    ),
                ),
            ],
            options={
                "ordering": ("-created_at", "-updated_at"),
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Parameter",
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
                ("name", models.CharField(max_length=100)),
                ("description", models.TextField(blank=True, null=True)),
                (
                    "node",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="parameters",
                        to="flow.nodeclass",
                    ),
                ),
            ],
            options={
                "ordering": ("-created_at", "-updated_at"),
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Connections",
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
                (
                    "source",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="connection_source",
                        to="flow.parameter",
                    ),
                ),
                (
                    "target",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="connection_target",
                        to="flow.parameter",
                    ),
                ),
            ],
            options={
                "ordering": ("-created_at", "-updated_at"),
                "abstract": False,
            },
        ),
    ]
