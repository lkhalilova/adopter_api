# Generated by Django 4.2.1 on 2023-05-30 23:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('adopter', '0003_anonymoususer'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='adopter',
            name='city',
        ),
    ]
