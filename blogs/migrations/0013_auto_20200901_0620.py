# Generated by Django 3.1 on 2020-09-01 06:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogs', '0012_auto_20200901_0616'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subscription',
            name='last_updated',
            field=models.DateTimeField(),
        ),
    ]