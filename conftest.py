import datetime
import pytest
import random
import uuid

from dateutil.relativedelta import relativedelta
from rest_framework.test import APIClient

from loan.models import Loans, Payments


@pytest.fixture
def api_client():
    return APIClient()


"""randomizers"""


@pytest.fixture(scope='function')
def randomizer():
    return Randomizer()


class Randomizer:

    def random_time_period(self):
        """ randomize digits"""
        digit = '123'
        return ''.join(random.choice(digit) for i in range(1))

    def random_digits_limit(self, limit):
        """ randomize digits"""
        digit = '123456789'
        return ''.join(random.choice(digit) for i in range(limit))

    def loan_data(self):
        data = {
            'loan_amount': self.random_digits_limit(4),
            'loan_start_date': datetime.date.today(),
            'periodicity_amount': self.random_digits_limit(2),
            'periodicity': self.random_time_period(),
            'number_of_payments': self.random_digits_limit(2),
            'interest_rate': self.random_digits_limit(2),
            'is_active': True
        }
        return data


@pytest.fixture(scope='function')
def custom_loan(randomizer):
    loan = Loans.objects.create(contract=uuid.uuid4(), **randomizer.loan_data())
    return loan


@pytest.fixture(scope='function')
def custom_payments(custom_loan, randomizer):
    payments = []
    new_amount = []
    for _ in range(10):
        amount = int(randomizer.random_digits_limit(3))
        payment = Payments(
            contract_id=custom_loan.id,
            payment_date=datetime.date.today() + relativedelta(days=10),
            principal_payment=amount,
            interest_payment=randomizer.random_digits_limit(2),
            is_active=True,
        )
        new_amount.append(amount)
        payments.append(payment)
    custom_loan.loan_amount = sum(new_amount)
    payments_qs = Payments.objects.bulk_create(payments)
    return payments_qs
