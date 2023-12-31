# Generated by Django 4.2.6 on 2023-12-22 16:33

import accounts.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_user_saved'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='pfp',
            field=models.ImageField(blank=True, default=None, null=True, upload_to=accounts.models.p, validators=[accounts.models.file_size_validate], verbose_name='profile picture'),
        ),
    ]
