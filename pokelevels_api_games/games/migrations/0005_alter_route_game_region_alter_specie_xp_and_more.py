# Generated by Django 5.0.6 on 2024-06-16 18:42

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('games', '0004_alter_gameregion_game_alter_gameregion_region_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='route',
            name='game_region',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='routes', to='games.gameregion'),
        ),
        migrations.AlterField(
            model_name='specie',
            name='xp',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='specie',
            name='xp1',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='specie',
            name='xp2',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='specie',
            name='xp3',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='specie',
            name='xp4',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='specie',
            name='xp5',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='specie',
            name='xp6',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='specie',
            name='xp7',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='specie',
            name='xp8',
            field=models.IntegerField(null=True),
        ),
    ]