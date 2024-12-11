# Generated by Django 5.1.4 on 2024-12-11 11:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('job', '0002_job_rated'),
    ]

    operations = [
        migrations.AlterField(
            model_name='job',
            name='schedule',
            field=models.CharField(choices=[('one_time', 'One-Time'), ('fulltime', 'Full-Time'), ('parttime', 'Part-Time'), ('internship', 'Internship'), ('project_work', 'Project-Work'), ('volunteering', 'Volunteering')], max_length=50),
        ),
    ]
