# Generated by Django 3.2.8 on 2022-04-22 15:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Criteria',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('level', models.IntegerField()),
                ('sigla', models.CharField(max_length=3)),
                ('criteria', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Quiz',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('data', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer', models.CharField(max_length=2)),
                ('criteria', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='assessment.criteria')),
                ('quiz', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='assessment.quiz')),
            ],
        ),
    ]
