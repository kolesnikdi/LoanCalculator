from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from LoanCalculator.constants import TimePeriod


class Loans(models.Model):
    contract = models.UUIDField('contract_number', default=None, null=True)
    loan_amount = models.DecimalField('loan_amount', max_digits=10, decimal_places=2)
    loan_start_date = models.DateField('start_loan')
    periodicity_amount = models.PositiveSmallIntegerField(
        'periodicity loan_amount',
        validators=[MaxValueValidator(365), MinValueValidator(1)],
    )
    periodicity = models.PositiveSmallIntegerField('periodicity', choices=TimePeriod.choices)
    number_of_payments = models.PositiveSmallIntegerField(validators=[MaxValueValidator(365), MinValueValidator(1)])
    interest_rate = models.DecimalField('interest_rate', max_digits=4, decimal_places=2)
    is_active = models.BooleanField(default=True)


class Payments(models.Model):
    contract = models.ForeignKey('loan.Loans', related_name='payments', on_delete=models.DO_NOTHING)
    payment_date = models.DateField('payment_date')
    principal_payment = models.DecimalField('principal_payment', max_digits=10, decimal_places=2)
    interest_payment = models.DecimalField('interest_payment', max_digits=10, decimal_places=2)
    is_active = models.BooleanField(default=True)
