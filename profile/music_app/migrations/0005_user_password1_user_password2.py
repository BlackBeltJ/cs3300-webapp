# Generated by Django 4.2 on 2024-04-08 23:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('music_app', '0004_user_alter_artist_profile'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='password1',
            field=models.CharField(default='password1234', max_length=200, verbose_name='password'),
        ),
        migrations.AddField(
            model_name='user',
            name='password2',
            field=models.CharField(default='password1234', max_length=200, verbose_name='confirm password'),
        ),
    ]
