# Generated by Django 5.1.1 on 2024-11-02 06:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('job', '0009_alter_job_created_at'),
    ]

    operations = [
        migrations.RenameField(
            model_name='job',
            old_name='job_type',
            new_name='tag',
        ),
    ]
