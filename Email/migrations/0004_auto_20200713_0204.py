# Generated by Django 3.0.8 on 2020-07-13 02:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Email', '0003_mail_sender_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='mail',
            name='sender_image',
        ),
        migrations.AddField(
            model_name='mail',
            name='file_upload',
            field=models.FileField(null=True, upload_to='files/'),
        ),
    ]
