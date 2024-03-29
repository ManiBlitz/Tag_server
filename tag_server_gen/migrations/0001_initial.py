# Generated by Django 2.1.2 on 2019-03-08 23:48

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type_game', models.IntegerField(default=1)),
                ('game_name', models.CharField(max_length=200)),
                ('duration', models.IntegerField(default=300)),
                ('game_status', models.IntegerField(default=1)),
            ],
        ),
        migrations.CreateModel(
            name='Lobby',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('game_started', models.BooleanField(default=False)),
                ('admin', models.BooleanField(default=False)),
                ('creation_time', models.DateTimeField(auto_now_add=True)),
                ('game', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tag_server_gen.Game')),
            ],
        ),
        migrations.CreateModel(
            name='Players',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('pseudoname', models.CharField(max_length=40)),
                ('email', models.EmailField(max_length=200, unique=True)),
                ('password', models.CharField(max_length=40)),
                ('phone_number', models.CharField(blank=True, max_length=17, validators=[django.core.validators.RegexValidator(message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.", regex='^\\+?1?\\d{9,15}$')])),
                ('date_creation', models.DateField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sender_id', models.IntegerField(max_length=11)),
                ('receipt_id', models.IntegerField(max_length=11)),
                ('game', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tag_server_gen.Game')),
            ],
        ),
        migrations.CreateModel(
            name='Teams',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('team_id', models.CharField(max_length=200)),
                ('game', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tag_server_gen.Game')),
                ('player', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tag_server_gen.Players')),
            ],
        ),
        migrations.AddField(
            model_name='lobby',
            name='player',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tag_server_gen.Players'),
        ),
    ]
