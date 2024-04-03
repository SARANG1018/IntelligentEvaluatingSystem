# Generated by Django 4.1.3 on 2023-05-05 17:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0002_question_difficulty'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='result',
            name='exam',
        ),
        migrations.RemoveField(
            model_name='result',
            name='marks',
        ),
        migrations.AddField(
            model_name='result',
            name='parent_list',
            field=models.JSONField(default=list),
        ),
    ]
