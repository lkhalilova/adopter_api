# Generated by Django 4.2.1 on 2023-05-29 13:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adopter', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='adopter',
            name='chat_id',
            field=models.BigIntegerField(blank=True, null=True),
        ),
    ]