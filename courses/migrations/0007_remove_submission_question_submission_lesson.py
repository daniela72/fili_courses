# Generated by Django 4.0.1 on 2022-03-12 20:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0006_submission_question'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='submission',
            name='question',
        ),
        migrations.AddField(
            model_name='submission',
            name='lesson',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='courses.lesson'),
            preserve_default=False,
        ),
    ]
