# Generated by Django 4.1 on 2022-08-20 07:52

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Skills',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('skill_name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='VendorModel',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, max_length=200, null=True)),
                ('location', models.CharField(blank=True, max_length=500, null=True)),
                ('rating', models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)])),
                ('skills', models.ManyToManyField(to='vendors.skills')),
            ],
            options={
                'db_table': 'vendor_details',
            },
        ),
    ]
