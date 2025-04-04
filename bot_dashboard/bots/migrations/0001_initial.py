# Generated by Django 5.1 on 2025-03-24 21:07

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
            name='FlaggedMessage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.BigIntegerField()),
                ('username', models.CharField(blank=True, max_length=255, null=True)),
                ('message', models.TextField()),
                ('reason', models.CharField(max_length=255)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('group_id', models.BigIntegerField(unique=True)),
                ('group_name', models.CharField(max_length=255)),
                ('total_users', models.IntegerField(default=0)),
                ('active_users', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='GroupSettings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('group_name', models.CharField(max_length=255)),
                ('faq_pdf', models.FileField(blank=True, null=True, upload_to='faq_pdfs/')),
                ('allow_links', models.BooleanField(default=True)),
                ('block_spam', models.BooleanField(default=True)),
                ('allow_promotions', models.BooleanField(default=False)),
                ('detect_deepfake', models.BooleanField(default=False)),
                ('detect_image_scam', models.BooleanField(default=False)),
            ],
        ),
    ]
