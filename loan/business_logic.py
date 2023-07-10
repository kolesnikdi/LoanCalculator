from dateutil.relativedelta import relativedelta
from LoanCalculator.constants import TimePeriod
from loan.models import Payments


def update_payments(contract, payment_id, subtract_sum):
    """
    :type contract: loan.models.Loans
    :type payment_id: int
    :type subtract_sum: decimal
    :type return: loan.models.Payments

    'Substract_sum' hhis is the amount by which need to reduce 'principal_payment'
    Creates new data to recreate payments.
    Load create_payments() with new data
    """
    payments = Payments.objects.filter(contract_id=contract.id, is_active=True, id__gte=payment_id)
    useful_payment = Payments.objects.filter(contract_id=contract.id, is_active=True, id__lt=payment_id).last()

    loan_data = {
        'loan_amount': sum((payment.principal_payment for payment in payments)),
        'periodicity': contract.periodicity,
        'number_of_payments': len(payments),
        'periodicity_amount': contract.periodicity_amount,
        'interest_rate': contract.interest_rate,
        'loan_start_date': useful_payment.payment_date,
    }
    payments.update(is_active=False)
    new_payments = create_payments(loan_data, contract.id, subtract_sum)
    return new_payments


def create_payments(loan_data, loan_id, substract_sum=None):
    """
    :type loan_data: loan.models.Loans
    :type loan_id: int
    :type substract_sum: decimal
    :type return: loan.models.Payments

    Create payments according to loan_data.
    Set loan_id to every payment
    'Substract_sum' needs only when use this function in update_payments()
    """
    less_amount = loan_data['loan_amount']
    periodicity = loan_data['periodicity']
    number_of_payments = loan_data['number_of_payments']
    periodicity_amount = loan_data['periodicity_amount']
    interest_rate = loan_data['interest_rate'] / 100

    if periodicity == TimePeriod.WEEK:
        update_payment_period = 'weeks'
        interest_period_rate = (periodicity_amount * interest_rate) / 52
    elif periodicity == TimePeriod.MONTH:
        update_payment_period = 'months'
        interest_period_rate = (periodicity_amount * interest_rate) / 12
    else:
        update_payment_period = 'days'
        interest_period_rate = (periodicity_amount * interest_rate) / 365

    payments = []
    for number in range(number_of_payments):
        number_left = number_of_payments - number
        payment_amount = round(
            interest_period_rate * less_amount / (1 - (1 + interest_period_rate) ** -number_left),
            2,
        )
        interest_payment = round(less_amount * interest_period_rate, 2)

        principal_payment = payment_amount - interest_payment
        if substract_sum is not None:
            principal_payment -= substract_sum
            substract_sum = None

        payment = Payments(
            contract_id=loan_id,
            payment_date=loan_data['loan_start_date'] + relativedelta(
                **{update_payment_period: (number + 1) * periodicity_amount}),
            interest_payment=interest_payment,
            principal_payment=principal_payment,
        )

        less_amount -= principal_payment
        payments.append(payment)

    return Payments.objects.bulk_create(payments)
