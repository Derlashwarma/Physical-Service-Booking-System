# Generated by Django 5.1.2 on 2024-11-02 18:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('job', '0012_alter_job_payment_method'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='job',
            name='job_type',
        ),
    ]