# Generated by Django 3.1.2 on 2020-10-25 13:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('covidyoddha', '0002_remove_patient_patient_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patient',
            name='patient',
            field=models.CharField(max_length=100, primary_key=True, serialize=False),
        ),
    ]
