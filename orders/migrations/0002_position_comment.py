# Generated by Django 2.2.5 on 2021-06-30 05:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='position',
            name='comment',
            field=models.CharField(blank=True, default='', max_length=120),
        ),
    ]