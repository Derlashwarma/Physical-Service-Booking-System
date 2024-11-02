# Generated by Django 5.1.2 on 2024-11-02 19:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('job', '0013_remove_job_job_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='job',
            name='category',
            field=models.CharField(default='plumbing', max_length=50),
        ),
        migrations.AlterField(
            model_name='job',
            name='payment_method',
            field=models.CharField(default='cash', max_length=20),
        ),
        migrations.AlterField(
            model_name='job',
            name='schedule',
            field=models.CharField(default='one_time', max_length=50),
        ),
    ]