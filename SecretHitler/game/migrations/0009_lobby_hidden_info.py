# Generated by Django 3.0.6 on 2020-06-22 00:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0008_auto_20200621_2121'),
    ]

    operations = [
        migrations.AddField(
            model_name='lobby',
            name='hidden_info',
            field=models.CharField(default='', max_length=100),
        ),
    ]