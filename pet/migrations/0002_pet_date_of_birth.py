# Generated by Django 5.0.2 on 2024-02-26 14:43

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pet', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='pet',
            name='date_of_birth',
            field=models.DateField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
