# Generated by Django 4.1.2 on 2022-10-07 04:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('campaigns', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='campaign',
            name='end_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='campaign',
            name='start_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]