from django.db import models
import datetime
from django.contrib.auth.models import Permission, User
from django.core.validators import RegexValidator
from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator,MaxValueValidator


class Main():
    phone_regex = RegexValidator(regex=r'^\+?1?\d{10}$', message="Numeric Field. Only 10 digits allowed.")

    exp_paid = (
        ('Bank','Bank'),
        ('Cash','Cash'),
        ('CreditCard','CreditCard')
               )
    exp_types =(
            ('ATM','ATM'),
            ('Entertainment','Entertainment'),
            ('groceries','groceries'),
            ('clothing','clothing'),
            ('recharge','recharge'),
            ('Bill','Bill'),
            ('others','others'),
                )
    inc_types =(
        ('Cash','Cash'),
        ('Bonus','Bonus'),
        ('Prize','Prize'),
               )


    debit_regex = RegexValidator(regex=r'^\+?1?\d{12}$', message="Numeric Field. Only 12 digits allowed.")


class UserDetails(models.Model):
    user = models.OneToOneField(User, default=1)
    #flag =models.IntegerField(default=0)

   # savings_per_year = models.PositiveIntegerField(default=10000)
    company_name=models.CharField(max_length=100)
    dob =models.DateField(null=True)
    address =models.CharField(max_length=100)
    hire_date =models.DateField(null=True)
    phone_no = models.IntegerField()
    photo =models.ImageField(upload_to='profile',default='\static\Main\images\noimage.png')
    occupation = models.CharField(max_length=15)
    yearly_package = models.PositiveIntegerField(null=True)
    pf = models.PositiveIntegerField(default=5)
    res_address = models.CharField(max_length=100)
    def __str__(self):
        return str(self.user)

class Balance(models.Model):
    user =models.OneToOneField(User,default=1)
    expense = models.FloatField(default=0)
    income = models.FloatField(default=0)
    total =models.FloatField(default=0)
  #  tax=models.FloatField(null=True)



    def __str__(self):
         return str(self.user)


class LoanPremium(models.Model,Main):
    user = models.ForeignKey(User, default=1)
    loan_premium_name = models.CharField(max_length=50,null=True)
    loan_premium_amount = models.PositiveIntegerField(null=True)
    start_date = models.DateField(null=True)
    end_date = models.DateField(default=2017-10-3,null=True)
    #vat_id=models.CharField(max_length=20,null=True)
    description=models.CharField(max_length=200,null=True)
    no_of_years = models.IntegerField(default=20,null=True)
    #date_of_payment = models.DateField(default=timezone.now)
    rate_of_interest = models.FloatField(default=10.0,null=True)
    type_loan_premium=models.CharField(max_length=15,null=True)
    type_duration = models.CharField(max_length=15,null=True)
    is_calender = models.BooleanField(default=False)

    def __str__(self):
        return str(self.user) + "__" + self.option + "__" + str(self.cost)

class Expense(models.Model):
    user = models.ForeignKey(User)
    subcategories = models.CharField(max_length=15)
    source = models.CharField(max_length=15)
    paid_to = models.CharField(max_length=50)
    cost = models.IntegerField()
    tax_details = models.FloatField()
    date_created = models.DateField(default =timezone.now)
    bill = models.FileField(null=True,blank=True,upload_to='bills')
    vat = models.CharField(max_length=50,null=True,blank=True)
    ext_ref = models.CharField(max_length=10,null=True,blank=True)
    description =models.CharField(max_length=100,null=True,blank=True)
    is_recurrent = models.CharField(max_length=10)
    rec_date=models.DateField(default=timezone.now)
    rec_year=models.IntegerField(null=True,blank=True)
    rec_month = models.IntegerField(null=True,blank=True)
    rec_day =models.IntegerField(null=True,blank=True)
    option = models.CharField(max_length=15)

    def __str__(self):
        return str(self.user)+"__"+self.option+"__"+str(self.cost)
