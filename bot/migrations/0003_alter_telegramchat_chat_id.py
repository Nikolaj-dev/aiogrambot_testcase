# Generated by Django 4.2.7 on 2023-11-15 14:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0002_remove_telegramchat_currency_history_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='telegramchat',
            name='chat_id',
            field=models.IntegerField(unique=True),
        ),
    ]