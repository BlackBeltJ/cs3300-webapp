# Generated by Django 4.2 on 2024-04-16 00:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('music_app', '0012_post_delete_project'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='mp3_file',
            field=models.FileField(blank=True, default='/static/audio/default_audio.mp3', upload_to='static/audio/'),
        ),
    ]
