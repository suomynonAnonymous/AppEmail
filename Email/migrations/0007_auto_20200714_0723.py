# Generated by Django 3.0.8 on 2020-07-14 07:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Email', '0006_auto_20200714_0717'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mail',
            name='subject',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]