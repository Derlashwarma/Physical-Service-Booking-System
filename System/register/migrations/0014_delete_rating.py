# Generated by Django 5.1.3 on 2024-11-09 10:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('register', '0013_alter_customuser_key_skills_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Rating',
        ),
    ]
