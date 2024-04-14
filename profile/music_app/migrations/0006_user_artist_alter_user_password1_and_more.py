# Generated by Django 4.2 on 2024-04-08 23:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('music_app', '0005_user_password1_user_password2'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='artist',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='music_app.artist'),
        ),
        migrations.AlterField(
            model_name='user',
            name='password1',
            field=models.CharField(default='change this', max_length=200, verbose_name='password'),
        ),
        migrations.AlterField(
            model_name='user',
            name='password2',
            field=models.CharField(default='change this', max_length=200, verbose_name='confirm password'),
        ),
    ]
