# Generated by Django 4.0.4 on 2022-05-06 04:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('jobsite', '0002_alter_jobsite_customer_jobsiteequipment'),
    ]

    operations = [
        migrations.AddField(
            model_name='jobsiteequipment',
            name='job_site',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='jobsite.jobsite'),
            preserve_default=False,
        ),
    ]
