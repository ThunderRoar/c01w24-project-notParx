# Generated by Django 4.1.13 on 2024-03-18 02:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_prescriber_verifiedprescriberid'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='csvfile',
            name='_id',
        ),
        migrations.RemoveField(
            model_name='csvfile',
            name='csv_file_id',
        ),
        migrations.AddField(
            model_name='csvfile',
            name='id',
            field=models.BigAutoField(auto_created=True, default='123', primary_key=True, serialize=False, verbose_name='ID'),
            preserve_default=False,
        ),
    ]
