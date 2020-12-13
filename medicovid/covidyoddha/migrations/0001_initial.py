# Generated by Django 3.1.2 on 2020-12-13 06:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Patient',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('patient_first_name', models.CharField(max_length=100)),
                ('patient_last_name', models.CharField(max_length=100)),
                ('patient_mobile', models.CharField(max_length=13)),
                ('patient_email', models.EmailField(max_length=254, null=True)),
                ('patient_age', models.IntegerField()),
                ('patient_gender', models.CharField(choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other')], help_text='Please select your Gender', max_length=1)),
            ],
        ),
        migrations.CreateModel(
            name='Staff',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone', models.CharField(max_length=13)),
                ('staff', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Report',
            fields=[
                ('report_id', models.UUIDField(default=uuid.uuid1, help_text='Unique ID for this particular report', primary_key=True, serialize=False)),
                ('result', models.CharField(choices=[('h', 'hold'), ('p', 'positive'), ('n', 'negative')], default='h', help_text='Status of the report', max_length=1)),
                ('file', models.FileField(upload_to='report/')),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='covidyoddha.patient')),
            ],
        ),
        migrations.CreateModel(
            name='Appointment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.DateTimeField()),
                ('patient', models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='covidyoddha.patient')),
            ],
        ),
    ]
