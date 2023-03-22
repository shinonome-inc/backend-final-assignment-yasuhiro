# Generated by Django 4.1.4 on 2023-03-22 00:18

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0001_initial"),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name="friendship",
            name="unique_friendship",
        ),
        migrations.AddField(
            model_name="friendship",
            name="data_created",
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]