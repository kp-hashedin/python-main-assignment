# Generated by Django 3.0.3 on 2022-09-15 17:03

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Logs',
            fields=[
                ('logs_id', models.AutoField(primary_key=True, serialize=False)),
                ('issue_id', models.IntegerField()),
                ('updated_field', models.CharField(max_length=20)),
                ('time_stamp', models.DateTimeField(auto_now=True)),
                ('previous_value', models.TextField()),
                ('updated_value', models.TextField()),
            ],
        ),
    ]
