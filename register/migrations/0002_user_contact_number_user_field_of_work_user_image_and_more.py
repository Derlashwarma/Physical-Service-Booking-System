# Generated by Django 5.1.1 on 2024-10-12 08:48

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('register', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='contact_number',
            field=models.CharField(default=2, max_length=11),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='user',
            name='field_of_work',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='user',
            name='image',
            field=models.ImageField(null=True, upload_to='images/'),
        ),
        migrations.AddField(
            model_name='user',
            name='is_worker',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='user',
            name='key_skills',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='user',
            name='previous_employment',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='user',
            name='professional_experience',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='user',
            name='professional_summary',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='user',
            name='social_contacts',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(blank=True, max_length=100),
        ),
        migrations.CreateModel(
            name='Rating',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('score', models.IntegerField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ratings_given', to='register.user')),
            ],
        ),
        migrations.AddField(
            model_name='user',
            name='ratings',
            field=models.ManyToManyField(blank=True, related_name='rated_users', to='register.rating'),
        ),
    ]
