from rest_framework import serializers

from loan.models import Loans, Payments


class LoanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Loans
        fields = ['contract', 'loan_amount', 'loan_start_date', 'periodicity_amount', 'periodicity',
                  'number_of_payments', 'interest_rate']
        extra_kwargs = {
            'contract': {'read_only': True},
        }


class PaymentsListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payments
        fields = ['id', 'payment_date', 'principal_payment', 'interest_payment']


class UpdatePaymentSerializer(serializers.Serializer):
    subtract_sum = serializers.DecimalField(max_digits=10, decimal_places=2)

    def validate(self, attrs):
        """The 'subtract sum' must be less than body of principal payment"""
        if payment := self.context.get('payment'):
            if attrs['subtract_sum'] > payment.principal_payment:
                raise serializers.ValidationError(
                    {"subtract_sum": f' Must be not bigger then {payment.principal_payment}.'},
                )
        return attrs
