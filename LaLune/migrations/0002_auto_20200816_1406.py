# Generated by Django 3.1 on 2020-08-16 12:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('LaLune', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='address',
            field=models.CharField(max_length=250, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='city',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='phone_number',
            field=models.CharField(max_length=12, null=True),
        ),
    ]
