# Generated by Django 3.1.2 on 2020-11-29 15:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('covidyoddha', '0003_auto_20201129_1100'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patient',
            name='patient_email',
            field=models.EmailField(max_length=254, null=True),
        ),
    ]