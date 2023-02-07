# Generated by Django 4.1.5 on 2023-01-27 19:11

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('LMS', '0002_remove_exam_class_grade_remove_exam_date_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='exam',
            name='class_grade',
            field=models.CharField(default=1, max_length=5),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='exam',
            name='date',
            field=models.CharField(default=1, max_length=20),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='exam',
            name='subject',
            field=models.CharField(default=1, max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='exam',
            name='teacher',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='examscore',
            name='exam_id',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='LMS.exam'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='examscore',
            name='exam_score',
            field=models.FloatField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='examscore',
            name='student',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='LMS.student'),
            preserve_default=False,
        ),
    ]