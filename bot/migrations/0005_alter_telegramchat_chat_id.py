# Generated by Django 4.2.7 on 2023-11-17 06:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0004_telegramchat_subscribed'),
    ]

    operations = [
        migrations.AlterField(
            model_name='telegramchat',
            name='chat_id',
            field=models.TextField(),
        ),
    ]
