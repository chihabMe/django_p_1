# Generated by Django 3.2.10 on 2022-03-21 06:45

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0017_alter_post_publish'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='publish',
            field=models.DateTimeField(default=datetime.datetime(2022, 3, 21, 6, 45, 56, 333550, tzinfo=utc)),
        ),
    ]
