# Generated by Django 3.0.5 on 2020-05-13 15:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('interface_app', '0004_dynamicprops'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='dynamicprops',
            name='greet',
        ),
    ]