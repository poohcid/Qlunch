# Generated by Django 3.0.3 on 2020-04-18 06:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appModel', '0010_auto_20200418_1355'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order_buffet',
            name='date',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='order_buffet',
            name='end_time',
            field=models.TimeField(),
        ),
        migrations.AlterField(
            model_name='order_buffet',
            name='start_time',
            field=models.TimeField(),
        ),
    ]
