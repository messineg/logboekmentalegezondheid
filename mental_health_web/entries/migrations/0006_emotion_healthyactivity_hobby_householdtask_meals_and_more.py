# Generated by Django 5.1.4 on 2025-01-16 17:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('entries', '0005_alter_advicefeedback_score'),
    ]

    operations = [
        migrations.CreateModel(
            name='Emotion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField()),
            ],
            options={
                'db_table': 'Emotions',
            },
        ),
        migrations.CreateModel(
            name='HealthyActivity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
            options={
                'db_table': 'HealthyActivities',
            },
        ),
        migrations.CreateModel(
            name='Hobby',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
            options={
                'db_table': 'Hobbies',
            },
        ),
        migrations.CreateModel(
            name='HouseholdTask',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
            options={
                'db_table': 'HouseholdTasks',
            },
        ),
        migrations.CreateModel(
            name='Meals',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
            options={
                'db_table': 'Meals',
            },
        ),
        migrations.CreateModel(
            name='PersonalGrowth',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
            options={
                'db_table': 'PersonalGrowth',
            },
        ),
        migrations.CreateModel(
            name='Productivity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
            options={
                'db_table': 'Productivity',
            },
        ),
        migrations.CreateModel(
            name='SleepQuality',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quality', models.IntegerField()),
            ],
            options={
                'db_table': 'SleepQuality',
            },
        ),
        migrations.CreateModel(
            name='SocialActivity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
            options={
                'db_table': 'SocialActivities',
            },
        ),
        migrations.CreateModel(
            name='Weather',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
            options={
                'db_table': 'Weather',
            },
        ),
        migrations.AddField(
            model_name='entry',
            name='emotions',
            field=models.ManyToManyField(to='entries.emotion'),
        ),
        migrations.AddField(
            model_name='entry',
            name='healthy_activities',
            field=models.ManyToManyField(to='entries.healthyactivity'),
        ),
        migrations.AddField(
            model_name='entry',
            name='hobbies',
            field=models.ManyToManyField(to='entries.hobby'),
        ),
        migrations.AddField(
            model_name='entry',
            name='household_tasks',
            field=models.ManyToManyField(to='entries.householdtask'),
        ),
        migrations.AddField(
            model_name='entry',
            name='meals',
            field=models.ManyToManyField(to='entries.meals'),
        ),
        migrations.AddField(
            model_name='entry',
            name='personal_growth',
            field=models.ManyToManyField(to='entries.personalgrowth'),
        ),
        migrations.AddField(
            model_name='entry',
            name='productivity',
            field=models.ManyToManyField(to='entries.productivity'),
        ),
        migrations.AddField(
            model_name='entry',
            name='sleep_quality',
            field=models.ManyToManyField(to='entries.sleepquality'),
        ),
        migrations.AddField(
            model_name='entry',
            name='social_activities',
            field=models.ManyToManyField(to='entries.socialactivity'),
        ),
        migrations.AddField(
            model_name='entry',
            name='weather',
            field=models.ManyToManyField(to='entries.weather'),
        ),
    ]
