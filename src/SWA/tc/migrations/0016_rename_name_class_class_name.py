# Generated by Django 4.1.2 on 2022-12-07 23:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tc', '0015_class_flight_operators'),
    ]

    operations = [
        migrations.RenameField(
            model_name='class',
            old_name='name',
            new_name='class_name',
        ),
    ]