# Generated by Django 3.0.3 on 2020-04-18 06:53

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appModel', '0008_auto_20200418_1150'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order_buffet',
            name='end_date',
        ),
        migrations.RemoveField(
            model_name='order_buffet',
            name='start_date',
        ),
        migrations.AddField(
            model_name='order_buffet',
            name='date',
            field=models.DateField(default=datetime.datetime(2020, 4, 18, 13, 53, 45, 44917)),
        ),
        migrations.AddField(
            model_name='order_buffet',
            name='end_time',
            field=models.TimeField(default=datetime.datetime(2020, 4, 18, 13, 53, 45, 44917)),
        ),
        migrations.AddField(
            model_name='order_buffet',
            name='start_time',
            field=models.TimeField(default=datetime.datetime(2020, 4, 18, 13, 53, 45, 44917)),
        ),
    ]
