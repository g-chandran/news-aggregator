# Generated by Django 3.1 on 2020-08-30 14:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Subscriptions',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('last_updated', models.CharField(max_length=35)),
                ('site_link', models.CharField(max_length=100)),
                ('feed_link', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Articles',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('published', models.CharField(max_length=35)),
                ('title', models.CharField(max_length=300)),
                ('author', models.CharField(default=' ', max_length=100)),
                ('summary', models.CharField(default=' ', max_length=500)),
                ('media', models.ImageField(upload_to='images/')),
                ('subscription_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blogs.subscriptions')),
            ],
        ),
    ]
