# Generated by Django 5.1.1 on 2024-11-01 10:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('job', '0006_alter_job_location'),
    ]

    operations = [
        migrations.AlterField(
            model_name='job',
            name='created_at',
            field=models.DateField(auto_now_add=True),
        ),
    ]
