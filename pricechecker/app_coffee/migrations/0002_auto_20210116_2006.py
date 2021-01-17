# Generated by Django 3.1.5 on 2021-01-16 13:06

from django.db import migrations, models
import django_countries.fields


class Migration(migrations.Migration):

    dependencies = [
        ('app_coffee', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='coffee',
            name='country_of_origin',
            field=django_countries.fields.CountryField(blank=True, max_length=2, verbose_name='Country of Origin'),
        ),
        migrations.AlterField(
            model_name='coffee',
            name='type',
            field=models.CharField(choices=[('UC', 'Unique Coffee'), ('BC', 'Black Coffee'), ('MC', 'Milk Based Coffee'), ('IC', 'Iced Coffee')], default='UC', max_length=2, verbose_name='Coffee Type'),
        ),
    ]
