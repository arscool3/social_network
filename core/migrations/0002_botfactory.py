# Generated by Django 4.0.4 on 2022-05-04 10:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='BotFactory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number_of_users', models.IntegerField()),
                ('max_posts', models.IntegerField()),
                ('max_likes', models.IntegerField()),
            ],
        ),
    ]
