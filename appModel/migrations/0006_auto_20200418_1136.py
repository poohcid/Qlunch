# Generated by Django 3.0.3 on 2020-04-18 04:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appModel', '0005_auto_20200418_1135'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order_buffet',
            name='end_date',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='order_buffet',
            name='start_date',
            field=models.DateTimeField(),
        ),
    ]