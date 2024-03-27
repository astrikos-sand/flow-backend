# Generated by Django 5.0.2 on 2024-03-27 19:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("flow", "0003_slot_speciality"),
    ]

    operations = [
        migrations.AlterField(
            model_name="slot",
            name="speciality",
            field=models.CharField(
                choices=[("DB", "Database"), ("WH", "Webhook"), ("NONE", "None")],
                default="NONE",
                max_length=10,
            ),
        ),
    ]
