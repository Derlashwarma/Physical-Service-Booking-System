# Generated by Django 5.1.2 on 2024-11-02 16:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('job', '0010_job_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='job',
            name='category',
            field=models.CharField(choices=[('plumbing', 'Plumbing'), ('babysitter', 'Babysitter'), ('landscaper', 'Landscaper'), ('laundry', 'Laundry'), ('house_keeping', 'House Keeping'), ('electrician', 'Electrician'), ('gardener', 'Gardener'), ('massage_therapist', 'Massage Therapist'), ('makeup_artist', 'Makeup Artist'), ('other', 'Other')], default='plumbing', max_length=50),
        ),
        migrations.AddField(
            model_name='job',
            name='payment_method',
            field=models.CharField(choices=[('cash', 'Cash'), ('gcash', 'GCash'), ('credit_debit', 'Credit/Debit')], default='cash', max_length=20),
        ),
        migrations.AddField(
            model_name='job',
            name='schedule',
            field=models.CharField(choices=[('one_time', 'One-Time'), ('fulltime', 'Full-Time'), ('parttime', 'Part-Time'), ('internship', 'Internship'), ('project_work', 'Project Work'), ('volunteering', 'Volunteering')], default='one_time', max_length=50),
        ),
    ]
