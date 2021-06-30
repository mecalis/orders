# Generated by Django 2.2.5 on 2021-06-10 10:45

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('meals', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='meal',
            name='day',
            field=models.DateField(blank=True, default=datetime.datetime.now),
        ),
        migrations.AlterField(
            model_name='meal',
            name='type',
            field=models.CharField(choices=[('1', 'állandó'), ('2', 'napi menü'), ('3', 'napi táblás'), ('4', 'egyéb')], max_length=1),
        ),
    ]