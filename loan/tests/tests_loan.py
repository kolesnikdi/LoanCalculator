import pytest
import uuid
from decimal import Decimal

from django.urls import reverse
from rest_framework import status

from loan.models import Loans


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
    def test_list_loan_valid(self, api_client, custom_loan, custom_payments):
        response = api_client.get(reverse('loan_payments', args=[custom_loan.contract]), format='json')
        response_json = response.json()
        assert response_json
        assert response_json['contract'] == str(custom_loan.contract)
        assert len(response_json['payments']) > 0
        assert response.status_code == status.HTTP_200_OK

    @pytest.mark.django_db
    def test_list_loan_invalid(self, api_client, custom_loan, custom_payments):
        response = api_client.get(reverse('loan_payments', args=['902999ff-37d7-4125-bd84-5aaf24f1f14a']), format='json')
        response_json = response.json()
        assert response_json
        assert response.status_code == status.HTTP_404_NOT_FOUND


class TestUpdatePaymentView:

    @pytest.mark.django_db
    def test_update_payment_invalid_id(self, api_client, custom_loan, custom_payments):
        data = {'subtract_sum': 50}
        response = api_client.post(reverse('payment', args=[11]), data=data, format='json')
        response_json = response.json()
        assert response_json
        assert response.status_code == status.HTTP_404_NOT_FOUND

    @pytest.mark.django_db
    def test_update_payment_invalid_subtract_sum(self, api_client, custom_loan, custom_payments):
        data = {'subtract_sum': 1000}
        response = api_client.post(reverse('payment', args=[custom_payments[2].id]), data=data, format='json')
        response_json = response.json()
        assert response_json
        assert response_json['subtract_sum'] == [f' Must be not bigger then {custom_payments[2].principal_payment}.00.']

    @pytest.mark.django_db
    def test_update_payment_valid(self, api_client, custom_loan, custom_payments):
        data = {'subtract_sum': 20}
        response = api_client.post(reverse('payment', args=[custom_payments[8].id]), data=data, format='json')
        response_json = response.json()
        assert response_json['contract']
        assert response_json['payments']
        assert response.status_code == status.HTTP_200_OK
        original_payment = custom_payments[8]
        update_payment = response_json['payments'][0]
        assert original_payment.id != update_payment['id']
        assert original_payment.payment_date != update_payment['payment_date']
        assert original_payment.principal_payment != update_payment['principal_payment']
        assert original_payment.interest_payment != update_payment['interest_payment']
