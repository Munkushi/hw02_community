# Generated by Django 2.2.9 on 2021-12-08 14:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0007_profile'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Profile',
        ),
    ]