# Generated by Django 2.0.5 on 2018-05-28 12:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('relreq', '0002_remove_dictgroup_rules'),
    ]

    operations = [
        migrations.AddField(
            model_name='dictgroup',
            name='parent',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
