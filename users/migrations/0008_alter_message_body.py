# Generated by Django 4.0.3 on 2022-06-12 06:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_user_blocked'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='body',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
    ]