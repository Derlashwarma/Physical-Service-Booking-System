# Generated by Django 5.1.1 on 2024-11-03 01:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('job', '0012_remove_job_is_active_remove_job_tag_job_category_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='job',
            name='category',
            field=models.CharField(choices=[('none', 'None'), ('repair', 'Repair'), ('cleaning_services', 'Cleaning Services'), ('massage', 'Massage'), ('childcare_services', 'Childcare Services'), ('carpentry', 'Carpentry'), ('other', 'Other')], default='none', max_length=50),
        ),
    ]
