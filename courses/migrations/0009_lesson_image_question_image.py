# Generated by Django 4.0.1 on 2022-04-10 21:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0008_remove_submission_lesson_submission_question'),
    ]

    operations = [
        migrations.AddField(
            model_name='lesson',
            name='image',
            field=models.CharField(default='none', max_length=2083),
        ),
        migrations.AddField(
            model_name='question',
            name='image',
            field=models.CharField(default='none', max_length=2083),
        ),
    ]