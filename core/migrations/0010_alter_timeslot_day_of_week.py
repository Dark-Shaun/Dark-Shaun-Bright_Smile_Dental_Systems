# Generated by Django 5.1.1 on 2024-09-22 00:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_alter_timeslot_day_of_week'),
    ]

    operations = [
        migrations.AlterField(
            model_name='timeslot',
            name='day_of_week',
            field=models.IntegerField(choices=[(0, 'Monday'), (1, 'Tuesday'), (2, 'Wednesday'), (3, 'Thursday'), (4, 'Friday'), (5, 'Saturday'), (6, 'Sunday')]),
        ),
    ]
