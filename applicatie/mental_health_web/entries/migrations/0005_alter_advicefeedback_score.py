# Generated by Django 5.1.4 on 2025-01-03 13:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('entries', '0004_advicefeedback'),
    ]

    operations = [
        migrations.AlterField(
            model_name='advicefeedback',
            name='score',
            field=models.IntegerField(blank=True, choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)], null=True),
        ),
    ]