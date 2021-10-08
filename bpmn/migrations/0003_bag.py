# Generated by Django 3.2.4 on 2021-10-08 10:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('bpmn', '0002_auto_20211008_0650'),
    ]

    operations = [
        migrations.CreateModel(
            name='Bag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('activities', models.ManyToManyField(to='bpmn.Activity')),
                ('container', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bpmn.flowelementscontainer')),
                ('group', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='auth.group')),
            ],
        ),
    ]
