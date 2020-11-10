# Generated by Django 3.1.2 on 2020-11-08 07:29

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('covidyoddha', '0007_auto_20201108_0707'),
    ]

    operations = [
        migrations.AlterField(
            model_name='report',
            name='file',
            field=models.FileField(upload_to='media/report/'),
        ),
        migrations.AlterField(
            model_name='report',
            name='report_id',
            field=models.UUIDField(default=uuid.uuid1, help_text='Unique ID for this particular report', primary_key=True, serialize=False),
        ),
    ]
