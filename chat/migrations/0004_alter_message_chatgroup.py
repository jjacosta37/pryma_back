# Generated by Django 3.2.8 on 2021-11-01 17:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0003_alter_message_sender'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='chatGroup',
            field=models.CharField(max_length=100),
        ),
    ]