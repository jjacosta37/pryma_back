# Generated by Django 3.2.8 on 2021-11-01 18:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0004_alter_message_chatgroup'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='content',
            field=models.TextField(default='prueba'),
            preserve_default=False,
        ),
    ]
