# Generated by Django 2.1.5 on 2019-03-12 16:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_auto_20190311_1258'),
    ]

    operations = [
        migrations.AddField(
            model_name='blog',
            name='video',
            field=models.FileField(blank=True, upload_to='blog_images'),
        ),
    ]
