# Generated by Django 3.1 on 2020-08-31 14:54

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('blogs', '0007_auto_20200831_1444'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='stored_time',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
