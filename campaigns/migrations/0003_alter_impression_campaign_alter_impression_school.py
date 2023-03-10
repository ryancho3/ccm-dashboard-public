# Generated by Django 4.1.2 on 2022-10-08 04:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('campaigns', '0002_campaign_end_date_campaign_start_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='impression',
            name='campaign',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='campaigns.campaign'),
        ),
        migrations.AlterField(
            model_name='impression',
            name='school',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='campaigns.school'),
        ),
    ]
