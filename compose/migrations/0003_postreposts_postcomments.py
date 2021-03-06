# Generated by Django 4.0.3 on 2022-04-10 14:28

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('compose', '0002_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PostReposts',
            fields=[
                ('created', models.DateTimeField(auto_now_add=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='compose.posts')),
                ('repost', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='postrepost', to='compose.posts')),
            ],
        ),
        migrations.CreateModel(
            name='PostComments',
            fields=[
                ('created', models.DateTimeField(auto_now_add=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('comment', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='postcomment', to='compose.posts')),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='compose.posts')),
            ],
        ),
    ]
