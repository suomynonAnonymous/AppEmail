# Generated by Django 3.0.8 on 2020-07-14 11:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Email', '0007_auto_20200714_0723'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mail',
            name='subject',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
