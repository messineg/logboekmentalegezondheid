# Generated by Django 5.1.4 on 2025-01-16 17:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('entries', '0007_remove_emotion_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sleepquality',
            name='quality',
            field=models.CharField(max_length=255),
        ),
    ]