# Generated by Django 5.0.2 on 2024-04-02 12:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("flow", "0016_remove_noderesult_value_noderesult_output"),
    ]

    operations = [
        migrations.RenameField(
            model_name="noderesult",
            old_name="output",
            new_name="inputs",
        ),
        migrations.AddField(
            model_name="noderesult",
            name="outputs",
            field=models.JSONField(blank=True, default=dict, null=True),
        ),
    ]