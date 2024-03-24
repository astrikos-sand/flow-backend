# Generated by Django 5.0.2 on 2024-03-16 06:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("flow", "0002_basenodeclass_genericnodeclass_triggernodeclass_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="slot",
            name="speciality",
            field=models.CharField(
                choices=[("DB", "Database"), ("NONE", "None")],
                default="NONE",
                max_length=10,
            ),
        ),
    ]
