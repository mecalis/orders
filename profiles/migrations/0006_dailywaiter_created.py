# Generated by Django 2.2.5 on 2021-08-23 14:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0005_auto_20210823_1557'),
    ]

    operations = [
        migrations.AddField(
            model_name='dailywaiter',
            name='created',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
