# Generated by Django 2.0.5 on 2018-05-28 00:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('relreq', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='dictgroup',
            name='rules',
        ),
    ]
