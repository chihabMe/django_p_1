# Generated by Django 3.2.10 on 2022-03-21 05:13

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0015_alter_post_publish'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='post',
            options={'ordering': ('-publish',)},
        ),
        migrations.AlterField(
            model_name='post',
            name='publish',
            field=models.DateTimeField(default=datetime.datetime(2022, 3, 21, 5, 13, 38, 21480, tzinfo=utc)),
        ),
    ]
