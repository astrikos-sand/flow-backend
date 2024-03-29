# Generated by Django 5.0.2 on 2024-03-28 04:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("flow", "0007_alter_slot_speciality"),
    ]

    operations = [
        migrations.AlterField(
            model_name="slot",
            name="speciality",
            field=models.CharField(
                choices=[
                    ("DB", "Database"),
                    ("API", "API"),
                    ("BACKEND", "Backend"),
                    ("NODE_ID", "Node ID"),
                    ("NONE", "None"),
                    ("SIG", "Signal"),
                ],
                default="NONE",
                max_length=10,
            ),
        ),
    ]