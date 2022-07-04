# Generated by Django 4.0.3 on 2022-05-01 14:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('compose', '0010_posts_blocked_users_remove_posts_post_privacy_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='posts',
            name='post_privacy',
            field=models.CharField(choices=[('public', 'public'), ('friends only', 'friends only'), ('only me', 'only me')], default='public', max_length=200),
        ),
    ]
