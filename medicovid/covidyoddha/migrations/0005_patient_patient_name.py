# Generated by Django 3.1.2 on 2020-10-25 13:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('covidyoddha', '0004_auto_20201025_1302'),
    ]

    operations = [
        migrations.AddField(
            model_name='patient',
            name='patient_name',
            field=models.CharField(default='Hari', max_length=100),
        ),
    ]
