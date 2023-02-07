# Generated by Django 4.1.5 on 2023-02-03 07:33

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('LMS', '0007_alter_examscore_exam_score'),
    ]

    operations = [
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('to', models.CharField(choices=[('همه کاربران', 'همه کاربران'), ('همه معلمان', 'همه معلمان'), ('همه دانش آموزان', 'همه دانش آموزان'), (models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL), models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL))], max_length=100)),
                ('message', models.TextField(max_length=600)),
                ('status', models.BooleanField()),
                ('reply', models.TextField(max_length=1000)),
                ('from_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]