# Generated by Django 4.1.13 on 2024-03-11 17:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='csvfile',
            old_name='file_location_with_status',
            new_name='new_file_location',
        ),
    ]
