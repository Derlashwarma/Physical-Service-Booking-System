# Generated by Django 5.1.3 on 2024-11-09 14:11

import ckeditor.fields
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Job',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('description', ckeditor.fields.RichTextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('is_active', models.BooleanField(default=True)),
                ('is_done', models.BooleanField(default=False)),
                ('budget', models.DecimalField(decimal_places=2, max_digits=100)),
                ('location', models.CharField(max_length=100)),
                ('finished_at', models.DateField(blank=True, null=True)),
                ('date', models.DateField(blank=True, null=True)),
                ('payment_method', models.CharField(choices=[('cash', 'Cash'), ('gcash', 'GCash'), ('credit_debit', 'Credit/Debit')], max_length=50)),
                ('category', models.CharField(choices=[('repair', 'Repair'), ('cleaning_services', 'Cleaning Services'), ('massage', 'Massage'), ('childcare_services', 'Childcare Services'), ('carpentry', 'Carpentry'), ('other', 'Other')], default='none', max_length=50)),
                ('schedule', models.CharField(choices=[('one_time', 'One-Time'), ('fulltime', 'Full-Time'), ('parttime', 'Part-Time')], max_length=50)),
                ('employer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='JobApplication',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('accepted', 'Accepted'), ('declined', 'Declined'), ('incomplete', 'Incomplete'), ('completed', 'Completed')], default='pending', max_length=10)),
                ('applied_at', models.DateTimeField(auto_now_add=True)),
                ('rated', models.BooleanField(default=False)),
                ('job', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='job.job')),
                ('worker', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
