# Generated by Django 4.1.5 on 2023-02-03 08:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('LMS', '0009_privateticket_publicticket_delete_ticket'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='publicticket',
            name='reply',
        ),
        migrations.RemoveField(
            model_name='publicticket',
            name='status',
        ),
    ]