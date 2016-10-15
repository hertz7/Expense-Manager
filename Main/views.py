from __future__ import print_function
import argparse
from reportlab.pdfgen import canvas

from googleapiclient.discovery import build
from httplib2 import Http

from oauth2client import file, client, tools
import webbrowser
from chartit.templatetags import chartit
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.shortcuts import render, redirect, render_to_response
from django.template import loader,RequestContext
from chartit import DataPool,Chart
from django.db.models.query import RawQuerySet
from django.db import connection
import simplejson
import json
from django.db.models import F,Sum,Q,aggregates, Count

from googleapiclient.discovery import build
from httplib2 import Http
import time
import argparse
import django.core.urlresolvers
from oauth2client.client import flow_from_clientsecrets
import oauth2client
from oauth2client import file, client, tools
import webbrowser
from chartit.templatetags import chartit
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.shortcuts import render, redirect, render_to_response,HttpResponseRedirect
from django.template import loader,RequestContext
from chartit import DataPool,Chart,PivotChart,PivotDataPool
import simplejson
import json,os
#from Main import client_secrets.json
from django.db.models import Aggregate
import argparse,httplib2
from oauth2client.tools import run_flow
import django_ipython
import ipython_genutils

# Create your views here.


from Main.forms import UserForm
from Main.models import Expense,Balance, UserDetails,User,LoanPremium

CLIENT_SECRETS = os.path.join(os.path.dirname(__file__), '..', 'client_secrets.json')
REDIRECT_URI = 'http://127.0.0.1:8000/Main/addloanpremium/'


def index(request):
    return render_to_response('Main/intro.html', locals(), context_instance=RequestContext(request))

def loginpage(request):
    return render_to_response('Main/login.html', locals(), context_instance=RequestContext(request))

def login_user(request):
    #if not request.user.is_authenticated():
    context =RequestContext(request)
    if request.method == "POST":
            username = request.POST.get('inputEmail')
            password = request.POST.get('inputPassword')
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    expenses = Expense.objects.filter(user=request.user).order_by('-date_created')
                    balances =Balance.objects.filter(user=request.user)
                    return render(request, 'Main/home_page.html',{'expenses':expenses[0:10],'balances':balances})
                else:
                    return render(request,'Main/login.html',{'error_message':'Your account has been disabled'})
            else:
                return render(request,'Main/login.html',{'error_message':'Invalid login'})
    else:
        return render(request,'Main/login.html')




def register_user(request):
    form = UserForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user.set_password(password)
        user.save()

        balance = Balance()
        user = User.objects.get(id=user.id)
        balance.user = user
        balance.income = 0
        balance.expense = 0
        balance.total=0
        balance.save()
       # user = authenticate(username=username, password=password)
        #if user is not None:
           # if user.is_active:
                #login(request, user)
               # owners = Owner.objects.filter(user=request.user)
        return render(request, 'Main/login.html',{})
    context = {
        "form": form,
    }
    return render(request,'Main/signup.html', context)

def exp_form(request):
    return render(request, 'Main/exp_form.html',None)
def loan_form(request):
    return render(request, 'Main/loan_pre_form.html',None)


def home_page(request):
    expenses = Expense.objects.filter(user=request.user).order_by('-date_created')
    balances = Balance.objects.filter(user=request.user)

    return render(request, 'Main/home_page.html',{'expenses':expenses[0:10],'balances':balances})

def save(request):

    return render(request, 'Main/home_page.html', {})

def log_out(request):
    logout(request)
    return render(request,'registration/logout.html')

def showtransactions(request):
    if request.method == 'POST':
        x = request.POST['date_in']
        y = request.POST['date_out']
        expenses = Expense.objects.filter(user=request.user).filter(date_created__range=[x,y])
        return render(request, 'Main/transactions.html', {'expenses': expenses})
    else:
        expenses=Expense.objects.filter(user=request.user).order_by('-date_created')
        return render(request,'Main/transactions.html',{'expenses':expenses})





def addexpense(request):
    if request.method == 'POST':
        expenses = Expense()

        user = request.user
        expenses.user = user

        expenses.paid_to = request.POST['expname']
        expenses.source = request.POST['cardtypexp']
        expenses.option = request.POST['types']


        expenses.date_created = request.POST['expdate']
        expenses.tax_details = request.POST['carddet']
        expenses.cost=  request.POST['amount']


        expenses.vat = request.POST['vat_id']
        expenses.ext_ref = request.POST['external_ref']
        expenses.description = request.POST['long_desc']
        if request.FILES['attachment_file']:
            expenses.bill = request.FILES['attachment_file']

        expenses.subcategories = request.POST['sub']
        expenses.is_recurrent = request.POST['is_recurrent']
        if expenses.is_recurrent == True:
            expenses.rec_date = request.POST['expdate']
            #expenses.rec_day = request.POST['rec_day']
            #expenses.rec_month = request.POST['rec_month']
            #expenses.rec_year = request.POST['rec_year']F
        expenses.save()
        x = expenses.cost

        try:
            balance = Balance.objects.filter(user=request.user).get(user_id=request.user.id)

            if expenses.option == 'Income':
                balance.income += int(x)
                balance.total += int(x)
            else:
                balance.expense += int(x)
                balance.total -= int(x)
            balance.save()
        except:
            balance = Balance()
            balance.user = request.user
            if expenses.option == 'Income':
                balance.income = x
                balance.expense = 0
                balance.total = x
                balance.save()
            else:
                balance.expense = x
                balance.income = 0
                balance.total = -int(x)
                balance.save()

        if (request.POST.get("is_recurrent") == "True"):
            print(" \n \n entered iscalendar =tru \n")

            print(" \n \n entered calendar now trying to add event \n \n")
            SCOPES = 'https://www.googleapis.com/auth/calendar'




            flow = flow_from_clientsecrets('D:\client_secrets.json', scope=SCOPES)
            storage = oauth2client.file.Storage('credentials.dat')
            # credentials = storage.get()
            http = httplib2.Http()
            flags = tools.argparser.parse_args(args=[])
            credentials = tools.run_flow(flow, storage, flags)
            # credentials = run(flow, storage, http=http)
            http = credentials.authorize(http)
            CAL = build('calendar', 'v3', http=http)
            dateString = ''
            dateString = request.POST.get('bday')
            dates = dateString[0:4] + dateString[5:7] + dateString[8:10]
            # ((int(request.GET.get('rate')))/100)

            print("\n  calendar was built successfully \n \n")
            GMT_OFF = '+05:30'  # PDT/MST/GMT-7
            EVENT = {
                'summary': 'Expense : ' + request.POST.get('expname') + ' Amount to be paid is ' +request.POST.get('amount') ,
                'start': {'date': request.POST.get('expdate')},
                'end': {'date': request.POST.get('expdate')},
                'recurrence': ['RRULE:FREQ=' + request.POST.get('etype')+';UNTIL='+dates],
            }

            e = CAL.events().insert(calendarId='primary',
                                    sendNotifications=True, body=EVENT).execute()
            print("\n \n event successfuly added \n \n")
            url = 'www.google.com/calendar'
            webbrowser.open_new(url)

    return render(request,'Main/exp_form.html',{})

def delete(request,ex_id):
    try:
        expenses = Expense.objects.filter(user=request.user).get(pk=ex_id)

        balance = Balance.objects.filter(user=request.user).get(user_id=request.user.id)
        x = expenses.cost
        if expenses.option == 'Expense':
            balance.expense -= x
            balance.total += x
        else:
            balance.income -= x
            balance.total -=x

        balance.save()
        expenses.delete()
        return redirect('Main:home_page')
    except:
        lp = LoanPremium.objects.filter(user=request.user).get(pk=ex_id)
        lp.delete()
        return redirect('Main:trans')


def getExpense(request):

    if request.method=='POST':
        x = request.POST['date_in']
        y = request.POST['date_out']
        weatherdata = \
            DataPool(
                series=
                [{'options': {
                    'source': Expense.objects.all().filter(user=request.user).filter(option__exact='Expense').filter(date_created__range=[x,y])},
                    'terms': [
                        {'expense': 'cost'},
                        {'date_expense': 'date_created'},
                    ]},
                    {'options': {
                        'source': Expense.objects.all().filter(user=request.user).filter(option__exact='Income').filter(date_created__range=[x,y])},
                        'terms': [
                            {'income': 'cost'},
                            {'date_income': 'date_created'},
                        ]}
                ])

        # Step 2: Create the Chart object
        cht = Chart(
            datasource=weatherdata,
            series_options=
            [{'options': {
                'type': 'column',
                'stacking': False},
                'terms': {
                    'date_expense': [
                        'expense',
                    ],
                    'date_income': [
                        'income']
                }}],
            chart_options=
            {'title': {
                'text': 'Income Vs Expenditure'},
                'xAxis': {
                    'title': {
                        'text': 'Date Created'}}})
        return render(request, 'Main/chart.html', {'cht': cht})


    # Step 1: Create a DataPool with the data we want to retrieve.
    else:
        weatherdata = \
                DataPool(
                    series=
                    [{'options': {
                        'source': Expense.objects.all().filter(user=request.user).filter(option__exact='Expense')},
                        'terms': [
                            {'expense': 'cost'},
                            {'date_expense': 'date_created'},
                        ]},
                        {'options': {
                            'source':Expense.objects.all().filter(user=request.user).filter(option__exact='Income')},
                            'terms': [
                                {'income': 'cost'},
                                {'date_income': 'date_created'},
                            ]}
                    ])

            # Step 2: Create the Chart object
        cht = Chart(
                datasource=weatherdata,
                series_options=
                [{'options': {
                    'type': 'column',
                    'stacking': False},
                    'terms':{
                  'date_expense': [
                    'expense',
                    ],
                  'date_income': [
                    'income']
                    }}],
                chart_options=
                {'title': {
                    'text': 'Income Vs Expenditure'},
                    'xAxis': {
                        'title': {
                            'text': 'Date Created'}}})
        return render(request, 'Main/chart.html', {'cht': cht})



def getExpense2(request):
    if request.method == 'POST':
        x = request.POST['date_in']
        y = request.POST['date_out']
        ds = DataPool(
            [{'options': {
                'source': Expense.objects.all().filter(user=request.user).filter(subcategories__exact='Entertainment').filter(date_created__range=[x,y])},
                'terms': [
                    {'Entertainment': 'cost'},
                    {'date': 'date_created'},
                ]},
                {'options': {
                    'source': Expense.objects.all().filter(user=request.user).filter(subcategories__exact='Health').filter(date_created__range=[x,y])},
                    'terms': [
                        {'Health': 'cost'},
                        {'date_e': 'date_created'},
                    ]},
                {'options': {
                    'source': Expense.objects.all().filter(user=request.user).filter(subcategories__exact='Education').filter(date_created__range=[x,y])},
                    'terms': [
                        {'Education': 'cost'},
                        {'date_i': 'date_created'},
                    ]},
                {'options': {
                    'source': Expense.objects.all().filter(user=request.user).filter(subcategories__exact='Travel').filter(date_created__range=[x,y])},
                    'terms': [
                        {'Travel': 'cost'},
                        {'date_g': 'date_created'},
                    ]},
                {'options': {
                    'source': Expense.objects.all().filter(user=request.user).filter(subcategories__exact='Lifestyle').filter(date_created__range=[x,y])},
                    'terms': [
                        {'Lifestyle': 'cost'},
                        {'date_h': 'date_created'},
                    ]},
                {'options': {
                    'source': Expense.objects.all().filter(user=request.user).filter(subcategories__exact='Food').filter(date_created__range=[x,y])},
                    'terms': [
                        {'Food': 'cost'},
                        {'date_k': 'date_created'},
                    ]},
                {'options': {
                    'source': Expense.objects.all().filter(user=request.user).filter(
                        subcategories__exact='Sports').filter(date_created__range=[x, y])},
                    'terms': [
                        {'Sports': 'cost'},
                        {'date_s': 'date_created'},
                    ]},
                {'options': {
                    'source': Expense.objects.all().filter(user=request.user).filter(
                        subcategories__exact='Loan and Premiums').filter(date_created__range=[x, y])},
                    'terms': [
                        {'Loan and Premiums': 'cost'},
                        {'date_p': 'date_created'},
                    ]},
            ])

        cht = Chart(
            datasource=ds,
            series_options=
            [{'options': {
                'type': 'column',
                'stacking': True},
                 'terms':{
                  'date': [
                    'Entertainment',
                    ],
                  'date_e': [
                    'Health'],
                     'date_i':[
                         'Education'
                     ],
                        'date_g':[
                            'Travel'
                        ],
                            'date_h':[
                                'Lifestyle'
                            ],
                                'date_k':[
                                    'Food'
                                ],
                     'date_s': [
                         'Sports'
                     ],
                     'date_p': [
                         'Loan and Premiums'
                     ]
                    }}],
            chart_options=
            {'title': {
                'text': 'Expenditure(Subcategories)'},
                'xAxis': {
                    'title': {
                        'text': 'Date Created'}}})
        return render(request, 'Main/chart2.html', {'cht': cht})
    else:
        ds = DataPool(
            [{'options': {
                'source': Expense.objects.all().filter(user=request.user).filter(subcategories__exact='Entertainment')},
                'terms': [
                    {'Entertainment': 'cost'},
                    {'date': 'date_created'},
                ]},
                {'options': {
                    'source': Expense.objects.all().filter(user=request.user).filter(subcategories__exact='Health')},
                    'terms': [
                        {'Health': 'cost'},
                        {'date_e': 'date_created'},
                    ]},
                {'options': {
                    'source': Expense.objects.all().filter(user=request.user).filter(subcategories__exact='Education')},
                    'terms': [
                        {'Education': 'cost'},
                        {'date_i': 'date_created'},
                    ]},
                {'options': {
                    'source': Expense.objects.all().filter(user=request.user).filter(subcategories__exact='Travel')},
                    'terms': [
                        {'Travel': 'cost'},
                        {'date_g': 'date_created'},
                    ]},
                {'options': {
                    'source': Expense.objects.all().filter(user=request.user).filter(subcategories__exact='Lifestyle')},
                    'terms': [
                        {'Lifestyle': 'cost'},
                        {'date_h': 'date_created'},
                    ]},
                {'options': {
                    'source': Expense.objects.all().filter(user=request.user).filter(subcategories__exact='Food')},
                    'terms': [
                        {'Food': 'cost'},
                        {'date_k': 'date_created'},
                    ]},
                {'options': {
                    'source': Expense.objects.all().filter(user=request.user).filter(
                        subcategories__exact='Sports')},
                    'terms': [
                        {'Sports': 'cost'},
                        {'date_s': 'date_created'},
                    ]},
                {'options': {
                    'source': Expense.objects.all().filter(user=request.user).filter(
                        subcategories__exact='Loan and Premiums')},
                    'terms': [
                        {'Loan and Premiums': 'cost'},
                        {'date_p': 'date_created'},
                    ]},
            ])

        cht = Chart(
            datasource=ds,
            series_options=
            [{'options': {
                'type': 'column',
                'stacking': True},
                'terms': {
                    'date': [
                        'Entertainment',
                    ],
                    'date_e': [
                        'Health'],
                    'date_i': [
                        'Education'
                    ],
                    'date_g': [
                        'Travel'
                    ],
                    'date_h': [
                        'Lifestyle'
                    ],
                    'date_k': [
                        'Food'
                    ],
                    'date_s': [
                        'Sports'
                    ],
                    'date_p': [
                        'Loan and Premiums'
                    ]
                }}],
            chart_options=
            {'title': {
                'text': 'Expenditure(Subcategories)'},
                'xAxis': {
                    'title': {
                        'text': 'Date Created'}}})
        return render(request, 'Main/chart2.html', {'cht': cht})


def addloanpremium(request):
    if request.method == 'GET':

       # premium = LoanPremium()
        user = request.user
        # form=loan_pre_form(request.POST)


        if (request.GET.get('typelp') == 'loan'):
            loan = LoanPremium()
            loan.user = user

            # premium.user=user
            print("\n \n entered loan now saving data \n \n")
            loan.type_loan_premium=request.GET.get('typelp')
            loan.loan_premium_name = request.GET.get('lpname')
            loan.loan_premium_amount = request.GET.get('lpamount')
            loan.start_date = request.GET.get('sdate')
            loan.end_date = request.GET.get('edate')
            loan.rate_of_interest = request.GET.get('rate')
            loan.description = request.GET.get('long_desc')
            loan.no_of_years = request.GET.get('years')
            ##rtype is for  monthly yearly daily
            loan.type_duration = request.GET.get('rtype')
            amt = (int(request.GET.get('lpamount'))) * (
            (1 + ((int(request.GET.get('rate'))) / 100)) * (int(request.GET.get('years'))))
            amt = amt / 12
            amt = int(amt)
            loan.save()
            dateString=''
            dateString=request.GET.get('edate')
            dates = dateString[0:4] + dateString[5:7] + dateString[8:10]
            print(" \n \n saved all data \n \n")
            # loan.no_of_years=request.POST['nyears']

            if (request.GET.get("iscalender") == "True"):
                print(" \n \n entered iscalendar =tru \n")

                print(" \n \n entered calendar now trying to add event \n \n")
                SCOPES = 'https://www.googleapis.com/auth/calendar'
                flow = flow_from_clientsecrets('D:\client_secrets.json',scope=SCOPES)
                storage = oauth2client.file.Storage('credentials.dat')
                # credentials = storage.get()
                http = httplib2.Http()
                flags = tools.argparser.parse_args(args=[])
                credentials = tools.run_flow(flow, storage, flags)
                # credentials = run(flow, storage, http=http)
                http = credentials.authorize(http)
                CAL = build('calendar', 'v3', http=http)

                # ((int(request.GET.get('rate')))/100)

                print("\n  calendar was built successfully \n \n")
                GMT_OFF = '+05:30'  # PDT/MST/GMT-7
                EVENT = {
                    'summary': 'Loan due to be paid: ' + request.GET.get('lpname') + ' Amount to be paid is ' + str(
                        amt),
                    'start': {'date': request.GET.get('sdate')},
                    'end': {'date': request.GET.get('sdate')},
                    'recurrence': ['RRULE:FREQ=' + request.GET.get('rtype')+';UNTIL='+dates+'T170000Z',],
                }

                e = CAL.events().insert(calendarId='primary',
                                        sendNotifications=True, body=EVENT).execute()
                print("\n \n event successfuly added \n \n")
                url = 'www.google.com/calendar'
                webbrowser.open_new(url)


        else:
            # loan.user=user
            premium = LoanPremium()
            user = request.user
            premium.type_loan_premium=request.GET.get('typelp')
            premium.user = user
            premium.loan_premium_name = request.GET.get('lpname')
            premium.loan_premium_amount = request.GET.get('lpamount')
            premium.start_date = request.GET.get('sdate')
            premium.end_date = request.GET.get('edate')
            premium.no_of_years = request.GET.get('years')
            # loan.rate_of_interest=request.POST['rate']
            premium.type_duration = request.GET.get('rtype')
            premium.description = request.GET.get('long_desc')
            # print (" \n\n "+request.GET.get('lpamount')+"\n\n")
             #amt=(int(request.GET.get('lpamount')))/12
            # amt=int(amt)
            premium.save()

            print("data was saved premium \n")
            # loan.loan_name=request.POST['lname']
            # loan.no_of_years=request.POST['nyears']
            if (request.GET.get("iscalender") == "True"):
                SCOPES = 'https://www.googleapis.com/auth/calendar'
                flow = flow_from_clientsecrets("D:\client_secrets.json", scope=SCOPES)
                storage = oauth2client.file.Storage('credentials.dat')
                # credentials = storage.get()
                http = httplib2.Http()
                flags = tools.argparser.parse_args(args=[])
                credentials = tools.run_flow(flow, storage, flags)
                # credentials = run(flow, storage, http=http)
                http = credentials.authorize(http)
                CAL = build('calendar', 'v3', http=http)
                dateString=''
                dateString = request.GET.get('edate')
                dates = dateString[0:4] + dateString[5:7] + dateString[8:10]
                print("\n  calendar was built successfully \n \n")
                GMT_OFF = '+05:30'  # PDT/MST/GMT-7
                EVENT = {
                    'summary': 'Premium due to be paid: ' + request.GET.get(
                        'lpname') + ' Amount to be paid is Rs ' +request.GET.get('lpamount') ,
                    'start': {'date': request.GET.get('sdate')},
                    'end': {'date': request.GET.get('sdate')},
                    'recurrence': ['RRULE:FREQ=' + request.GET.get('rtype')+';UNTIL='+dates+'T170000Z'],
                }

                e = CAL.events().insert(calendarId='primary',
                                        sendNotifications=True, body=EVENT).execute()
                print("\n \n event successfuly added \n \n")
                url = 'www.google.com/calendar'
                webbrowser.open_new(url)

        return render_to_response('Main/loan_pre_form.html', {})


def editprofile(request):
   # if request.method=='POST':

    userdetails = UserDetails.objects.filter(user=request.user).get(user_id=request.user.id)

    return render(request,'Main/editprofile.html',{'userdetails':userdetails})

def profile(request):
    try:
        userdetails = UserDetails.objects.get(user=request.user)

    except UserDetails.DoesNotExist:
       return render(request,'Main/editprofile.html',{})
    return render(request, 'Main/profile.html', {'userdetails': userdetails})

def update(request,ex_id):
    if request.method=='POST':
        try:

            userdetails = UserDetails.objects.filter(user=request.user).get(user_id=request.user.id)
            userdetails.address=request.POST['com_add']
            userdetails.dob=request.POST['dob']
            userdetails.company_name=request.POST['company']
            userdetails.res_address=request.POST['res_add']
            userdetails.phone_no=request.POST['ph_no']
            userdetails.hire_date=request.POST['doj']
            userdetails.yearly_package=request.POST['yp']
            userdetails.dob=request.POST['dob']
            userdetails.occupation=request.POST['position']
            # x = userdetails.photo
            # userdetails.photo.delete()
            if request.FILES['photo']:
                userdetails.photo=userdetails.photo
            else:
                userdetails.photo=request.FILES['photo']
            userdetails.save()
            u=User.objects.get(pk=ex_id)
            u.first_name = request.POST['fname']
            u.last_name = request.POST['lname']
            u.username = request.POST['username']
            u.save()

            return render(request, 'Main/home_page.html', {'userdetails': userdetails})


        except:

            userdetails=UserDetails()

            userdetails.user=request.user
            userdetails.address = request.POST['com_add']
            userdetails.dob = request.POST['dob']
            userdetails.company_name = request.POST['company']
            userdetails.res_address = request.POST['res_add']
            userdetails.phone_no = request.POST['ph_no']
            userdetails.hire_date = request.POST['doj']
            userdetails.yearly_package = request.POST['yp']
            userdetails.dob = request.POST['dob']
            userdetails.occupation = request.POST['position']
            userdetails.photo=request.FILES['photo']

            userdetails.save()
            u = User.objects.get(pk=ex_id)
            u.first_name = request.POST['fname']
            u.last_name = request.POST['lname']
            u.username = request.POST['username']
            u.save()
            return render(request, 'Main/home_page.html', {'userdetails': userdetails})

def lpfilter(request):

    if request.method == 'POST':
         x = request.POST['date_in']
         y = request.POST['date_out']
         premiums = LoanPremium.objects.filter(user=request.user).filter(start_date__range=[x, y])
         return render(request, 'Main/loanpremiumtransaction.html', {'premiums': premiums})
    else:
        premiums = LoanPremium.objects.filter(user=request.user).order_by('-start_date')
        return render(request, 'Main/loanpremiumtransaction.html', {'premiums': premiums})


def transactions(request):
    premiums=LoanPremium.objects.all().filter(user=request.user)
    return render(request,'Main/loanpremiumtransaction.html',{'premiums':premiums})


def delete_user(request,u_id):
    u = User.objects.get(pk=u_id)
    u.delete()
    return render(request,'Main/Intro.html',{})

def pdf(request):
    response = HttpResponse(content_type='app/pdf')
    response['Content-Disposition'] = 'attachment; filename="somefilename.pdf"'
    p = canvas.Canvas(response)


    p.drawCentredString(100, 100,'hello world')

    p.showPage()
    p.save()
    return response



