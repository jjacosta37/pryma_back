# Generated by Django 3.2.8 on 2021-11-08 16:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0008_alter_supplier_groupname'),
    ]

    operations = [
        migrations.AlterField(
            model_name='supplier',
            name='groupname',
            field=models.CharField(blank=True, editable=False, max_length=500),
        ),
    ]
