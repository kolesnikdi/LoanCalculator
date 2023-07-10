import uuid
from django.db import transaction

from rest_framework import generics, status
from rest_framework.response import Response

from loan.models import Loans, Payments
from loan.business_logic import create_payments, update_payments
from loan.serializers import LoanSerializer, PaymentsListSerializer, UpdatePaymentSerializer


class CreateLoanView(generics.CreateAPIView):
    """Only post method.
    Create: loan, payments to loan.
    Returns: Loan.data and all payments to this loan.
    """
    serializer_class = LoanSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            with transaction.atomic():
                new_loan = Loans.objects.create(contract=uuid.uuid4(), **serializer.validated_data)
                payments = create_payments(serializer.validated_data, new_loan.id)
                response = self.serializer_class(instance=new_loan).data
                #
                response["payments"] = PaymentsListSerializer(payments, many=True).data
                res_status = status.HTTP_200_OK
        except Exception as e:
            response = {'error': 'Something went wrong. Contact the site administrator.'}
            res_status = status.HTTP_400_BAD_REQUEST
        return Response(response, status=res_status)


class UpdatePaymentView(generics.CreateAPIView):
    """Only post method.
    Updates the payment body specified in the url...<id>.
    Payment must be active.
    Recalculates the current and subsequent payments and recreates them.
    Returns: Loan.data and all payments that was changed
    """
    serializer_class = UpdatePaymentSerializer
    queryset = Payments.objects.all()
    lookup_field = 'id'

    def post(self, request, *args, **kwargs):
        payment = self.get_object()
        if not payment.is_active:
            return Response({'error': 'Not valid payment id.'}, status=status.HTTP_400_BAD_REQUEST)
        loan = payment.contract
        serializer = self.serializer_class(data=request.data, context={'payment': payment})
        serializer.is_valid(raise_exception=True)
        try:
            payments = update_payments(loan, payment.id, serializer.validated_data['subtract_sum'])
            response = LoanSerializer(loan).data
            response["payments"] = PaymentsListSerializer(payments, many=True).data
            res_status = status.HTTP_200_OK
        except Exception as e:
            response = {'error': 'Something went wrong. Contact the site administrator.'}
            res_status = status.HTTP_400_BAD_REQUEST
        return Response(response, status=res_status)


class ListLoanView(generics.RetrieveAPIView):
    """List loan data and all payments of this loan"""
    serializer_class = LoanSerializer
    queryset = Loans.objects.all()
    lookup_field = 'contract'

    def get(self, request, *args, **kwargs):
        loan = self.get_object()
        payments = Payments.objects.filter(contract_id=loan.id, is_active=True)
        response = self.serializer_class(instance=loan).data
        response["payments"] = PaymentsListSerializer(payments, many=True).data
        return Response(response, status=status.HTTP_200_OK)
