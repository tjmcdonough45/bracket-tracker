# Generated by Django 2.1.1 on 2019-01-07 11:22

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('BracketApp', '0004_point'),
    ]

    operations = [
        migrations.AddField(
            model_name='bracket',
            name='submitted',
            field=models.DateField(default=datetime.datetime(2019, 1, 7, 11, 22, 18, 61879, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='season',
            name='premiere',
            field=models.DateField(default=datetime.datetime(2019, 1, 7, 11, 22, 18, 61879, tzinfo=utc)),
        ),
    ]
