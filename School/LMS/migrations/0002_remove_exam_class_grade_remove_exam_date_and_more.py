# Generated by Django 4.1.5 on 2023-01-27 19:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('LMS', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='exam',
            name='class_grade',
        ),
        migrations.RemoveField(
            model_name='exam',
            name='date',
        ),
        migrations.RemoveField(
            model_name='exam',
            name='subject',
        ),
        migrations.RemoveField(
            model_name='exam',
            name='teacher',
        ),
        migrations.RemoveField(
            model_name='examscore',
            name='exam_id',
        ),
        migrations.RemoveField(
            model_name='examscore',
            name='exam_score',
        ),
        migrations.RemoveField(
            model_name='examscore',
            name='student',
        ),
    ]