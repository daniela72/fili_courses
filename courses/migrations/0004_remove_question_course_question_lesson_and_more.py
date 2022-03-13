# Generated by Django 4.0.1 on 2022-03-07 01:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0003_alter_instructor_total_learners'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='question',
            name='course',
        ),
        migrations.AddField(
            model_name='question',
            name='lesson',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='courses.lesson'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='course',
            name='name',
            field=models.CharField(default='Course/Grade', max_length=30),
        ),
        migrations.AlterField(
            model_name='question',
            name='question_text',
            field=models.CharField(default='Question', max_length=200),
        ),
    ]
