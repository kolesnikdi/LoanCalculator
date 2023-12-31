# Generated by Django 4.1.2 on 2023-07-11 06:48

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Loans',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contract', models.UUIDField(default=None, null=True, verbose_name='contract_number')),
                ('loan_amount', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='loan_amount')),
                ('loan_start_date', models.DateField(verbose_name='start_loan')),
                ('periodicity_amount', models.PositiveSmallIntegerField(validators=[django.core.validators.MaxValueValidator(365), django.core.validators.MinValueValidator(1)], verbose_name='periodicity loan_amount')),
                ('periodicity', models.PositiveSmallIntegerField(choices=[(1, 'Day'), (2, 'Week'), (3, 'Month')], verbose_name='periodicity')),
                ('number_of_payments', models.PositiveSmallIntegerField(validators=[django.core.validators.MaxValueValidator(365), django.core.validators.MinValueValidator(1)])),
                ('interest_rate', models.DecimalField(decimal_places=2, max_digits=4, verbose_name='interest_rate')),
                ('is_active', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Payments',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('payment_date', models.DateField(verbose_name='payment_date')),
                ('principal_payment', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='principal_payment')),
                ('interest_payment', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='interest_payment')),
                ('is_active', models.BooleanField(default=True)),
                ('contract', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='payments', to='loan.loans')),
            ],
        ),
    ]
