# Generated by Django 4.1.7 on 2023-03-24 11:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tokenblacklist',
            name='token',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
