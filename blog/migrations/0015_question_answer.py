# Generated by Django 2.1.5 on 2019-04-12 22:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0014_question_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='answer',
            field=models.TextField(blank=True),
        ),
    ]
