# Generated by Django 3.2.5 on 2021-08-21 15:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0003_bid'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='first_bid',
            field=models.IntegerField(default=0),
        ),
    ]
