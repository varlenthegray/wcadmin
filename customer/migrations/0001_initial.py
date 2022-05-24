# Generated by Django 4.0.4 on 2022-05-24 19:50

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quickbooks_id', models.IntegerField(blank=True, editable=False, null=True)),
                ('company', models.CharField(blank=True, max_length=100, null=True)),
                ('title', models.CharField(blank=True, max_length=30, null=True)),
                ('first_name', models.CharField(max_length=100)),
                ('middle_name', models.CharField(blank=True, max_length=100, null=True)),
                ('last_name', models.CharField(max_length=100)),
                ('secondary_contact_name', models.CharField(blank=True, max_length=100, null=True)),
                ('website', models.URLField(blank=True, null=True)),
                ('email', models.EmailField(max_length=254)),
                ('main_phone', models.CharField(blank=True, max_length=15, null=True)),
                ('alternate_phone', models.CharField(blank=True, max_length=15, null=True)),
                ('fax_number', models.CharField(blank=True, max_length=15, null=True)),
                ('billing_address_same_as_jobsite', models.BooleanField(blank=True, default=False, null=True)),
                ('billing_address_1', models.CharField(blank=True, max_length=200, null=True)),
                ('billing_address_2', models.CharField(blank=True, max_length=200, null=True)),
                ('billing_city', models.CharField(blank=True, max_length=100, null=True)),
                ('billing_state', models.CharField(blank=True, max_length=2, null=True)),
                ('billing_zip', models.CharField(blank=True, max_length=10, null=True)),
                ('is_active', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='CustomerNotes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.CharField(max_length=100)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('note', models.TextField()),
                ('created_by', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='customer.customer')),
            ],
        ),
    ]
