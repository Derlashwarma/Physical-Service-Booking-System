# Generated by Django 5.1.1 on 2024-10-27 07:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('job', '0002_job_location'),
    ]

    operations = [
        migrations.AddField(
            model_name='job',
            name='job_type',
            field=models.CharField(default='No Value', max_length=50),
            preserve_default=False,
        ),
    ]
