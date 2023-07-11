import pytest
import uuid
from decimal import Decimal

from django.urls import reverse
from rest_framework import status

from loan.models import Loans, Payments


class TestCreateLoanView:
    """Invalid data stops on serializers level"""

    @pytest.mark.django_db
    def test_create_loan_valid(self, api_client, randomizer):
        data = randomizer.loan_data()
        response = api_client.post(reverse('create_loan'), data=data, format='json')
        response_json = response.json()
        assert response_json
        assert response.status_code == status.HTTP_200_OK
        assert len(response_json['payments']) > 0
        data_for_check_loan = Loans.objects.filter(is_active=True).last()
        assert data_for_check_loan.loan_amount == Decimal(data["loan_amount"])
        assert data_for_check_loan.loan_start_date == data['loan_start_date']
        assert data_for_check_loan.periodicity_amount == int(data['periodicity_amount'])
        assert data_for_check_loan.periodicity == int(data['periodicity'])
        assert data_for_check_loan.number_of_payments == int(data['number_of_payments'])
        assert data_for_check_loan.interest_rate == int(data['interest_rate'])
        assert data_for_check_loan.is_active is True
        assert isinstance(data_for_check_loan.contract, uuid.UUID)

class TestListLoanView:

    @pytest.mark.django_db
    def test_list_loan_valid(self, client_with_loan_payments):
        contract = client_with_loan_payments.loan.contract
        response = client_with_loan_payments.get(reverse('loan_payments', args=[contract]), format='json')
        response_json = response.json()
        assert response_json
        assert response_json['contract'] == str(contract)
        assert len(response_json['payments']) > 0
        assert response.status_code == status.HTTP_200_OK

    @pytest.mark.django_db
    def test_list_loan_invalid(self, client_with_loan_payments):
        url = reverse('loan_payments', args=['902999ff-37d7-4125-bd84-5aaf24f1f14a'])
        response = client_with_loan_payments.get(url, format='json')
        response_json = response.json()
        assert response_json
        assert response.status_code == status.HTTP_404_NOT_FOUND


class TestUpdatePaymentView:

    @pytest.mark.django_db
    def test_update_payment_invalid_id(self, client_with_loan_payments):
        payment_id = client_with_loan_payments.pyaments[8].id
        data = {'subtract_sum': 50}
        response = client_with_loan_payments.post(reverse('payment', args=[payment_id*10]), data=data, format='json')
        response_json = response.json()
        assert response_json
        assert response.status_code == status.HTTP_404_NOT_FOUND

    @pytest.mark.django_db
    def test_update_payment_invalid_subtract_sum(self, client_with_loan_payments):
        payment_id = client_with_loan_payments.pyaments[8].id
        principal_payment = client_with_loan_payments.pyaments[8].principal_payment
        data = {'subtract_sum': client_with_loan_payments.pyaments[8].principal_payment + 1}
        response = client_with_loan_payments.post(reverse('payment', args=[payment_id]), data=data, format='json')
        response_json = response.json()
        assert response_json
        assert response_json['subtract_sum'] == [f' Must be not bigger then {principal_payment}.']

    @pytest.mark.django_db
    def test_update_payment_valid(self, client_with_loan_payments):
        original_payment = {
            'id': client_with_loan_payments.pyaments[8].id,
            'payment_date': client_with_loan_payments.pyaments[8].payment_date,
            'principal_payment': client_with_loan_payments.pyaments[8].principal_payment,
            'interest_payment': client_with_loan_payments.pyaments[8].interest_payment,
            'is_active': client_with_loan_payments.pyaments[8].is_active,
        }
        data = {'subtract_sum': original_payment['principal_payment'] - 1}
        url = reverse('payment', args=[original_payment['id']])
        response = client_with_loan_payments.post(url, data=data, format='json')
        response_json = response.json()
        assert response_json['contract']
        assert response_json['payments']
        assert response.status_code == status.HTTP_200_OK
        update_payment = response_json['payments'][0]
        assert original_payment['id'] != update_payment['id']
        assert str(original_payment['payment_date']) == update_payment['payment_date']
        assert original_payment['principal_payment'] != Decimal(update_payment['principal_payment'])
        assert update_payment['principal_payment'] == '1.00'
        assert original_payment['interest_payment'] == Decimal(update_payment['interest_payment'])
        old_payment = Payments.objects.get(id=original_payment['id'])
        assert old_payment.is_active is False
