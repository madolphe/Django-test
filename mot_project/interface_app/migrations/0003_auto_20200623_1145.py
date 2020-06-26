# Generated by Django 3.0.5 on 2020-06-23 11:45

from django.db import migrations
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('interface_app', '0002_auto_20200623_0938'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='study',
            name='extra',
        ),
        migrations.AddField(
            model_name='experimentsession',
            name='extra_json',
            field=jsonfield.fields.JSONField(default=dict),
        ),
        migrations.AddField(
            model_name='study',
            name='extra_json',
            field=jsonfield.fields.JSONField(default=dict),
        ),
        migrations.AlterField(
            model_name='participantprofile',
            name='extra_json',
            field=jsonfield.fields.JSONField(default=dict),
        ),
    ]
