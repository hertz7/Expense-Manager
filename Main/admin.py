from django.contrib import admin

# Register your models here.
from Main.models import Expense,LoanPremium,UserDetails
admin.site.register(Expense)
admin.site.register(LoanPremium)
admin.site.register(UserDetails)
