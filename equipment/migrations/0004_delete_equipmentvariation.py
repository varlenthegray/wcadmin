# Generated by Django 4.0.4 on 2022-05-09 02:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('equipment', '0003_alter_equipment_sku_alter_equipmentvariation_sku'),
    ]

    operations = [
        migrations.DeleteModel(
            name='EquipmentVariation',
        ),
    ]