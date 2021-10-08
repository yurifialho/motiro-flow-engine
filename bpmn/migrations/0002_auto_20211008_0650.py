# Generated by Django 3.2.8 on 2021-10-08 09:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('kipco', '0001_initial'),
        ('auth', '0012_alter_user_first_name_max_length'),
        ('bpmn', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='flowelementscontainer',
            name='goal',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='kipco.processgoal'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='lane',
            name='group',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='auth.group'),
            preserve_default=False,
        ),
    ]