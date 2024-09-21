# Generated by Django 5.0.2 on 2024-09-21 10:32

import apps.flow.utils
import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("contenttypes", "0002_remove_content_type_name"),
    ]

    operations = [
        migrations.CreateModel(
            name="BaseNode",
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
                (
                    "position",
                    models.JSONField(default=apps.flow.utils.default_position),
                ),
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
        ),
        migrations.CreateModel(
            name="Dependency",
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
                ("name", models.CharField(max_length=100, unique=True)),
                ("requirements", models.FileField(upload_to="flow/dependencies/")),
            ],
            options={
                "verbose_name": "Dependency",
                "verbose_name_plural": "Dependencies",
            },
        ),
        migrations.CreateModel(
            name="FileArchive",
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
                ("name", models.CharField(max_length=255)),
                ("file", models.FileField(upload_to="uploads/")),
            ],
            options={
                "ordering": ("-created_at", "-updated_at"),
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="FunctionDefinition",
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
                ("name", models.CharField(max_length=255, unique=True)),
                ("description", models.TextField(blank=True, null=True)),
                ("code", models.FileField(upload_to="flow/functions/")),
            ],
            options={
                "ordering": ("-created_at", "-updated_at"),
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="ConditionalNode",
            fields=[
                (
                    "basenode_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="flow.basenode",
                    ),
                ),
                (
                    "value_type",
                    models.CharField(
                        choices=[
                            ("INT", "Integer"),
                            ("STR", "String"),
                            ("BOOL", "Boolean"),
                            ("FLOAT", "Float"),
                            ("LIST", "List"),
                            ("SET", "Set"),
                            ("TUPLE", "Tuple"),
                            ("DICT", "Dictionary"),
                            ("NONE", "None"),
                            ("ANY", "Any"),
                        ],
                        max_length=15,
                    ),
                ),
                ("name", models.CharField(blank=True, max_length=255, null=True)),
            ],
            options={
                "ordering": ("-created_at", "-updated_at"),
                "abstract": False,
            },
            bases=("flow.basenode",),
        ),
        migrations.CreateModel(
            name="DataNode",
            fields=[
                (
                    "basenode_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="flow.basenode",
                    ),
                ),
                ("name", models.CharField(max_length=255)),
                ("value", models.CharField(max_length=10000)),
                (
                    "value_type",
                    models.CharField(
                        choices=[
                            ("INT", "Integer"),
                            ("STR", "String"),
                            ("BOOL", "Boolean"),
                            ("FLOAT", "Float"),
                            ("LIST", "List"),
                            ("SET", "Set"),
                            ("TUPLE", "Tuple"),
                            ("DICT", "Dictionary"),
                            ("NONE", "None"),
                            ("ANY", "Any"),
                        ],
                        max_length=15,
                    ),
                ),
            ],
            options={
                "ordering": ("-created_at", "-updated_at"),
                "abstract": False,
            },
            bases=("flow.basenode",),
        ),
        migrations.CreateModel(
            name="InputNode",
            fields=[
                (
                    "basenode_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="flow.basenode",
                    ),
                ),
            ],
            options={
                "ordering": ("-created_at", "-updated_at"),
                "abstract": False,
            },
            bases=("flow.basenode",),
        ),
        migrations.CreateModel(
            name="OutputNode",
            fields=[
                (
                    "basenode_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="flow.basenode",
                    ),
                ),
            ],
            options={
                "ordering": ("-created_at", "-updated_at"),
                "abstract": False,
            },
            bases=("flow.basenode",),
        ),
        migrations.CreateModel(
            name="Flow",
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
                ("name", models.CharField(max_length=255)),
                ("description", models.TextField(blank=True, null=True)),
                (
                    "lib",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="flows",
                        to="flow.dependency",
                    ),
                ),
                (
                    "scope",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="local_flows",
                        to="flow.flow",
                    ),
                ),
            ],
            options={
                "ordering": ("-created_at", "-updated_at"),
                "abstract": False,
            },
        ),
        migrations.AddField(
            model_name="basenode",
            name="flow",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="nodes",
                to="flow.flow",
            ),
        ),
        migrations.CreateModel(
            name="FunctionField",
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
                ("name", models.CharField(max_length=255)),
                (
                    "attachment_type",
                    models.CharField(
                        choices=[("IN", "Input"), ("OUT", "Output")], max_length=10
                    ),
                ),
                (
                    "value_type",
                    models.CharField(
                        choices=[
                            ("INT", "Integer"),
                            ("STR", "String"),
                            ("BOOL", "Boolean"),
                            ("FLOAT", "Float"),
                            ("LIST", "List"),
                            ("SET", "Set"),
                            ("TUPLE", "Tuple"),
                            ("DICT", "Dictionary"),
                            ("NONE", "None"),
                            ("ANY", "Any"),
                        ],
                        default="ANY",
                        max_length=15,
                    ),
                ),
                (
                    "definition",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="fields",
                        to="flow.functiondefinition",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="ScopeBlock",
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
                (
                    "flow",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="scope_block",
                        to="flow.flow",
                    ),
                ),
            ],
            options={
                "ordering": ("-created_at", "-updated_at"),
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Slot",
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
                ("name", models.CharField(max_length=255)),
                (
                    "attachment_type",
                    models.CharField(
                        choices=[("IN", "Input"), ("OUT", "Output")], max_length=10
                    ),
                ),
                (
                    "value_type",
                    models.CharField(
                        choices=[
                            ("INT", "Integer"),
                            ("STR", "String"),
                            ("BOOL", "Boolean"),
                            ("FLOAT", "Float"),
                            ("LIST", "List"),
                            ("SET", "Set"),
                            ("TUPLE", "Tuple"),
                            ("DICT", "Dictionary"),
                            ("NONE", "None"),
                            ("ANY", "Any"),
                        ],
                        default="ANY",
                        max_length=15,
                    ),
                ),
                (
                    "node",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="slots",
                        to="flow.basenode",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Connection",
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
                (
                    "from_slot",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="connections_out",
                        to="flow.slot",
                    ),
                ),
                (
                    "to_slot",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="connections_in",
                        to="flow.slot",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Tag",
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
                ("name", models.CharField(max_length=255)),
                (
                    "parent",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="flow.tag",
                    ),
                ),
            ],
            options={
                "verbose_name": "Tag",
                "verbose_name_plural": "Tags",
            },
        ),
        migrations.CreateModel(
            name="BaseModelWithTag",
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
                ("tags", models.ManyToManyField(blank=True, to="flow.tag")),
            ],
            options={
                "ordering": ("-created_at", "-updated_at"),
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="BlockNode",
            fields=[
                (
                    "basenode_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="flow.basenode",
                    ),
                ),
                (
                    "block",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="block_node",
                        to="flow.scopeblock",
                    ),
                ),
            ],
            options={
                "ordering": ("-created_at", "-updated_at"),
                "abstract": False,
            },
            bases=("flow.basenode",),
        ),
        migrations.CreateModel(
            name="ConditionalNodeCase",
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
                ("value", models.CharField(blank=True, max_length=255, null=True)),
                (
                    "block",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="conditional_node_case",
                        to="flow.scopeblock",
                    ),
                ),
                (
                    "node",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="cases",
                        to="flow.conditionalnode",
                    ),
                ),
            ],
            options={
                "ordering": ("-created_at", "-updated_at"),
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="FlowNode",
            fields=[
                (
                    "basenode_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="flow.basenode",
                    ),
                ),
                (
                    "represent",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="represent_nodes",
                        to="flow.flow",
                    ),
                ),
            ],
            options={
                "ordering": ("-created_at", "-updated_at"),
                "abstract": False,
            },
            bases=("flow.basenode",),
        ),
        migrations.CreateModel(
            name="ForEachNode",
            fields=[
                (
                    "basenode_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="flow.basenode",
                    ),
                ),
                (
                    "block",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="for_each_node",
                        to="flow.scopeblock",
                    ),
                ),
            ],
            options={
                "ordering": ("-created_at", "-updated_at"),
                "abstract": False,
            },
            bases=("flow.basenode",),
        ),
        migrations.CreateModel(
            name="FunctionNode",
            fields=[
                (
                    "basenode_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="flow.basenode",
                    ),
                ),
                (
                    "definition",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="nodes",
                        to="flow.functiondefinition",
                    ),
                ),
            ],
            options={
                "ordering": ("-created_at", "-updated_at"),
                "abstract": False,
            },
            bases=("flow.basenode",),
        ),
        migrations.AddIndex(
            model_name="basenode",
            index=models.Index(fields=["flow"], name="flow_baseno_flow_id_dcf66d_idx"),
        ),
        migrations.AddIndex(
            model_name="functionfield",
            index=models.Index(
                fields=["definition"], name="flow_functi_definit_47aced_idx"
            ),
        ),
        migrations.AlterUniqueTogether(
            name="functionfield",
            unique_together={("name", "definition", "attachment_type")},
        ),
        migrations.AddIndex(
            model_name="slot",
            index=models.Index(fields=["node"], name="flow_slot_node_id_aea239_idx"),
        ),
        migrations.AlterUniqueTogether(
            name="slot",
            unique_together={("name", "node", "attachment_type")},
        ),
        migrations.AlterUniqueTogether(
            name="connection",
            unique_together={("from_slot", "to_slot")},
        ),
        migrations.AddIndex(
            model_name="tag",
            index=models.Index(fields=["name"], name="flow_tag_name_374358_idx"),
        ),
        migrations.AddIndex(
            model_name="tag",
            index=models.Index(fields=["parent"], name="flow_tag_parent__4766af_idx"),
        ),
        migrations.AlterUniqueTogether(
            name="tag",
            unique_together={("name", "parent")},
        ),
    ]
