# Generated by Django 5.0.6 on 2024-06-03 17:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='grand_total',
            field=models.FloatField(default=10),
            preserve_default=False,
        ),
    ]