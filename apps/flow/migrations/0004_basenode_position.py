# Generated by Django 5.0.2 on 2024-03-26 22:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("flow", "0003_slot_speciality"),
    ]

    operations = [
        migrations.AddField(
            model_name="basenode",
            name="position",
            field=models.JSONField(default={"x": 0, "y": 0}),
        ),
    ]
