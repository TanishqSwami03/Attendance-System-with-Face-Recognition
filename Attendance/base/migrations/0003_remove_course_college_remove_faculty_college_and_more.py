# Generated by Django 5.0.4 on 2024-05-13 17:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0002_alter_college_options_alter_college_managers_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='course',
            name='college',
        ),
        migrations.RemoveField(
            model_name='faculty',
            name='College',
        ),
        migrations.RemoveField(
            model_name='student',
            name='college',
        ),
        migrations.RemoveField(
            model_name='attendance',
            name='college',
        ),
        migrations.DeleteModel(
            name='College',
        ),
    ]