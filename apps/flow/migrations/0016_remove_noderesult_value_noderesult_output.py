# Generated by Django 5.0.2 on 2024-04-02 12:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("flow", "0015_alter_noderesult_node"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="noderesult",
            name="value",
        ),
        migrations.AddField(
            model_name="noderesult",
            name="output",
            field=models.JSONField(blank=True, default=dict, null=True),
        ),
    ]