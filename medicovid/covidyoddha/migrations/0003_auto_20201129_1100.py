# Generated by Django 3.1.2 on 2020-11-29 11:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('covidyoddha', '0002_patient_patient_otp'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='patient',
            name='patient_otp',
        ),
        migrations.AlterField(
            model_name='appointment',
            name='patient',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='covidyoddha.patient'),
        ),
    ]