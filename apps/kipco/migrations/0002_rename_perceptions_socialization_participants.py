# Generated by Django 3.2.8 on 2022-04-27 01:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('kipco', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='socialization',
            old_name='perceptions',
            new_name='participants',
        ),
    ]
