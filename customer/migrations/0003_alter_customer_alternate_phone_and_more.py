# Generated by Django 4.0.3 on 2022-04-10 01:05

from django.db import migrations, models
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0002_customer_primary_technician_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='alternate_phone',
            field=phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, region=None),
        ),
        migrations.AlterField(
            model_name='customer',
            name='fax_number',
            field=phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, region=None),
        ),
        migrations.AlterField(
            model_name='customer',
            name='middle_name',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='customer',
            name='secondary_contact_name',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='customer',
            name='website',
            field=models.URLField(blank=True),
        ),
    ]