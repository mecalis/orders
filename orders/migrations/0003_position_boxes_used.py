# Generated by Django 2.2.5 on 2021-07-22 09:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0002_position_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='position',
            name='boxes_used',
            field=models.IntegerField(blank=True, default=0),
        ),
    ]
