# Generated by Django 5.0.2 on 2024-06-22 17:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("flow", "0024_alter_slot_speciality"),
    ]

    operations = [
        migrations.AlterField(
            model_name="datanode",
            name="value",
            field=models.CharField(max_length=10000),
        ),
    ]
