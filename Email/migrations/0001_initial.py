# Generated by Django 3.0.8 on 2020-07-12 12:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Mail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(choices=[('support', 'Support'), ('assignment', 'Assignment'), ('examination', 'Examination'), ('practical', 'Practical')], max_length=50)),
                ('subject', models.CharField(max_length=500)),
                ('body', models.TextField()),
                ('send_date', models.DateTimeField(blank=True, null=True)),
                ('received_date', models.DateTimeField(auto_now=True)),
                ('mail_send', models.BooleanField(default=False)),
                ('starred', models.BooleanField(default=False)),
                ('spam', models.BooleanField(default=False)),
                ('mail_deleted', models.BooleanField(default=False)),
                ('receiver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='mail_requests_receiver', to=settings.AUTH_USER_MODEL)),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='mail_requests_sender', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
