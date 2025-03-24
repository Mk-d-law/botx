# Generated by Django 5.1 on 2025-03-24 11:06

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Bot',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bot_token', models.CharField(max_length=255, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='BotSettings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('group_name', models.CharField(max_length=255)),
                ('moderation_level', models.IntegerField(default=1)),
                ('auto_delete_spam', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='GroupSettings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('group_id', models.BigIntegerField(unique=True)),
                ('group_name', models.CharField(max_length=255)),
                ('allow_links', models.BooleanField(default=True)),
                ('block_spam', models.BooleanField(default=True)),
                ('allow_promotions', models.BooleanField(default=False)),
            ],
        ),
    ]
