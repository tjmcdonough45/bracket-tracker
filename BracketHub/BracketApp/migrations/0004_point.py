# Generated by Django 2.1.1 on 2019-01-07 05:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('BracketApp', '0003_season_season_pic'),
    ]

    operations = [
        migrations.CreateModel(
            name='Point',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rank', models.PositiveIntegerField(default=69)),
                ('elimination', models.PositiveIntegerField(default=69)),
                ('points_per_contestant_remaining', models.PositiveIntegerField(default=0)),
                ('num_boots', models.PositiveIntegerField(default=0)),
                ('season', models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='BracketApp.Season')),
            ],
            options={
                'ordering': ['elimination'],
            },
        ),
    ]
