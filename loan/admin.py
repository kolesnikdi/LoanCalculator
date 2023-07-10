from django.contrib import admin
from loan.models import Loans, Payments

# Register your models here.

admin.site.register(Loans)
admin.site.register(Payments)
