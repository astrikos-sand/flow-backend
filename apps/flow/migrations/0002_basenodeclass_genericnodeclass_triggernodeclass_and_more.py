# Generated by Django 5.0.2 on 2024-03-15 21:45

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("contenttypes", "0002_remove_content_type_name"),
        ("flow", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="BaseNodeClass",
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
                (
                    "polymorphic_ctype",
                    models.ForeignKey(
                        editable=False,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="polymorphic_%(app_label)s.%(class)s_set+",
                        to="contenttypes.contenttype",
                    ),
                ),
            ],
            options={
                "ordering": ("-created_at", "-updated_at"),
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="GenericNodeClass",
            fields=[
                (
                    "basenodeclass_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="flow.basenodeclass",
                    ),
                ),
            ],
            options={
                "ordering": ("-created_at", "-updated_at"),
                "abstract": False,
            },
            bases=("flow.basenodeclass",),
        ),
        migrations.CreateModel(
            name="TriggerNodeClass",
            fields=[
                (
                    "basenodeclass_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="flow.basenodeclass",
                    ),
                ),
            ],
            options={
                "ordering": ("-created_at", "-updated_at"),
                "abstract": False,
            },
            bases=("flow.basenodeclass",),
        ),
        migrations.RenameModel(
            old_name="DynamicNode",
            new_name="GenericNode",
        ),
        migrations.AlterField(
            model_name="genericnode",
            name="node_class",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="nodes",
                to="flow.basenodeclass",
            ),
        ),
        migrations.AlterField(
            model_name="slot",
            name="node_class",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="slots",
                to="flow.basenodeclass",
            ),
        ),
        migrations.DeleteModel(
            name="DynamicNodeClass",
        ),
    ]
