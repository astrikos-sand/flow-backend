# Generated by Django 5.0.2 on 2024-12-23 07:51

import apps.flow.utils
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("flow", "0009_alter_dependency_requirements_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="filearchive",
            name="file",
            field=models.FileField(upload_to=apps.flow.utils.archive_upload_path),
        ),
    ]
