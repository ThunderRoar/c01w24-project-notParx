# Generated by Django 4.1.13 on 2024-03-12 21:34

from django.db import migrations
import djongo.models.fields


class Migration(migrations.Migration):
    dependencies = [
        ("api", "0008_remove_user_perscribersid"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="prescribersID",
            field=djongo.models.fields.JSONField(default=list),
        ),
    ]
