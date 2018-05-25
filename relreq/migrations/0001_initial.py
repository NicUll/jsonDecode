# Generated by Django 2.0.5 on 2018-05-25 15:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Connection',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hostname', models.CharField(max_length=200)),
                ('hosturl', models.CharField(max_length=200)),
                ('restuser', models.CharField(max_length=20)),
                ('restpass', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='DictGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=40)),
                ('dictentryid', models.IntegerField(blank=True, null=True)),
                ('rules', models.CharField(blank=True, max_length=20, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='JsonDictionaryEntry',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('jsonvalue', models.CharField(max_length=20)),
                ('displayvalue', models.CharField(max_length=40)),
                ('haschildren', models.BooleanField()),
                ('parent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='relreq.DictGroup')),
            ],
        ),
    ]