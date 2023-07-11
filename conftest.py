import datetime
import pytest
import random
import uuid
from dateutil.relativedelta import relativedelta

from django.urls import reverse
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
            'loan_amount': self.random_digits_limit(6),
            'loan_start_date': datetime.date.today(),
            'periodicity_amount': self.random_digits_limit(2),
            'periodicity': self.random_time_period(),
            'number_of_payments': self.random_digits_limit(2),
            'interest_rate': self.random_digits_limit(2),
            'is_active': True
        }
        return data


@pytest.fixture(scope='function')
def client_with_loan_payments(api_client, randomizer):
    response = api_client.post(reverse('create_loan'), data=randomizer.loan_data(), format='json')
    api_client.loan = Loans.objects.filter(is_active=True).last()
    api_client.pyaments = Payments.objects.filter(contract=api_client.loan, is_active=True)
    return api_client
