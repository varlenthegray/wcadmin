# Generated by Django 4.0.4 on 2022-04-22 00:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0008_alter_customer_access_code_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='alternate_phone',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
        migrations.AlterField(
            model_name='customer',
            name='fax_number',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
        migrations.AlterField(
            model_name='customer',
            name='main_phone',
            field=models.CharField(max_length=15),
        ),
    ]
