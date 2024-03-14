# Generated by Django 5.0.2 on 2024-03-11 12:38

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("resource", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="resourcegroup",
            name="name",
            field=models.CharField(
                db_index=True,
                max_length=255,
                validators=[
                    django.core.validators.RegexValidator(
                        "/", inverse_match=True, message="name can't contain '/'"
                    )
                ],
            ),
        ),
    ]