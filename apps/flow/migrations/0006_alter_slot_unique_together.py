# Generated by Django 5.0.2 on 2024-03-28 00:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("flow", "0005_alter_slot_options_alter_slot_speciality_and_more"),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name="slot",
            unique_together={("name", "node_class")},
        ),
    ]
