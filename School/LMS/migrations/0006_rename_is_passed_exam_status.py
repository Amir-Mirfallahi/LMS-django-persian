# Generated by Django 4.1.5 on 2023-01-28 14:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('LMS', '0005_exam_descriptions'),
    ]

    operations = [
        migrations.RenameField(
            model_name='exam',
            old_name='is_passed',
            new_name='status',
        ),
    ]
