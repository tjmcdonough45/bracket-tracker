# Generated by Django 2.1.1 on 2019-10-02 22:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BracketApp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='contestant',
            name='contestant_pic',
            field=models.URLField(default='https://wwwimage-secure.cbsstatic.com/thumbnails/photos/w400/cast/svr_cast_800x1000_0018_mollybyman.jpg'),
        ),
    ]
