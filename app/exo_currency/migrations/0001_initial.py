# Generated by Django 2.2.13 on 2020-06-22 13:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Currency',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=3, unique=True)),
                ('name', models.CharField(db_index=True, max_length=20)),
                ('symbol', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Provider',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(choices=[('Fixer', 'exo_currency.utils.fixer_currency_exchanger.FixerCurrencyExchanger'), ('Mock', 'exo_currency.utils.mock_currency_exchanger.MockCurrencyExchanger')], max_length=20, unique=True)),
                ('order', models.PositiveIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='CurrencyExchangeRate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('valuation_date', models.DateField(db_index=True)),
                ('rate_value', models.DecimalField(db_index=True, decimal_places=6, max_digits=18)),
                ('exchanged_currency', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='exo_currency.Currency')),
                ('source_currency', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='exchanges', to='exo_currency.Currency')),
            ],
        ),
    ]
