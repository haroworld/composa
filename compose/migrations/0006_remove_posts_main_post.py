# Generated by Django 4.0.3 on 2022-04-10 18:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('compose', '0005_posts_main_post'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='posts',
            name='main_post',
        ),
    ]
