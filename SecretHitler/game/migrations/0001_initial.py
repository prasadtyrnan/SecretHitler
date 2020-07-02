# Generated by Django 3.0.6 on 2020-06-01 02:03

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Lobby',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('room_num', models.IntegerField()),
                ('num_players', models.IntegerField()),
                ('player_one', models.CharField(max_length=100)),
                ('player_two', models.CharField(max_length=100)),
                ('player_three', models.CharField(max_length=100)),
                ('player_four', models.CharField(max_length=100)),
                ('player_five', models.CharField(max_length=100)),
                ('player_six', models.CharField(max_length=100)),
                ('player_seven', models.CharField(max_length=100)),
                ('player_eight', models.CharField(max_length=100)),
            ],
        ),
    ]
