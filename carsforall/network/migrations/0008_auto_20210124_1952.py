# Generated by Django 3.1.1 on 2021-01-24 14:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0007_car_renter_wish'),
    ]

    operations = [
        migrations.RenameField(
            model_name='car',
            old_name='renter_wish',
            new_name='renters_wished',
        ),
    ]
