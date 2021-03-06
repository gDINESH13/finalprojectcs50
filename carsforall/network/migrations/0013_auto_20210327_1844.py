# Generated by Django 3.1.1 on 2021-03-27 13:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0012_remove_car_past_renters'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='message',
            field=models.CharField(blank=True, max_length=400),
        ),
        migrations.AlterField(
            model_name='car',
            name='curr_time_rent',
            field=models.DateTimeField(blank=True, default=None),
        ),
    ]
