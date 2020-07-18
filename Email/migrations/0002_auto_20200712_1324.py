# Generated by Django 3.0.8 on 2020-07-12 13:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Email', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='mail',
            old_name='received_date',
            new_name='viewed_date',
        ),
        migrations.AlterField(
            model_name='mail',
            name='label',
            field=models.CharField(choices=[('SP', 'Support'), ('AS', 'Assignment'), ('EX', 'Examination'), ('PR', 'Practical')], max_length=2),
        ),
        migrations.AlterField(
            model_name='mail',
            name='send_date',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
