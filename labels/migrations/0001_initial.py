# Generated by Django 3.0.3 on 2022-09-15 11:25

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Label',
            fields=[
                ('label_id', models.AutoField(primary_key=True, serialize=False)),
                ('label', models.CharField(max_length=50)),
                ('issue_id', models.IntegerField()),
            ],
        ),
    ]