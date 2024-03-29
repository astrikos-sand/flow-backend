# Generated by Django 5.0.2 on 2024-03-27 23:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("flow", "0004_alter_slot_speciality"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="slot",
            options={},
        ),
        migrations.AlterField(
            model_name="slot",
            name="speciality",
            field=models.CharField(
                choices=[("DB", "Database"), ("SIG", "Signal"), ("NONE", "None")],
                default="NONE",
                max_length=10,
            ),
        ),
        migrations.AlterUniqueTogether(
            name="slot",
            unique_together={("name", "node_class", "attachment_type")},
        ),
    ]