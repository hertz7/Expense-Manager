from django.conf.urls import url
from django.contrib import admin
from Main import views
app_name ='Main'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^home/$',views.login_user,name='home'),
    url(r'^register_user/$',views.register_user,name='register_user'),
    url(r'^home_page/$',views.home_page,name='home_page'),
    url(r'^save/$',views.save,name='save'),
    url(r'^loginpage/$',views.loginpage,name='loginpage'),
    url(r'^exp_form/$',views.exp_form,name='exp_form'),
    url(r'^logout/$',views.log_out,name='logout'),
    url(r'^addexpense/$',views.addexpense,name='addexpense'),
    url(r'^chart/$',views.getExpense,name='getExpense'),
    url(r'^delete/(?P<ex_id>\d+)$',views.delete,name='delete'),
    url(r'^transactions/$',views.showtransactions,name='transactions'),
    url(r'^addloanpremium/$', views.addloanpremium, name='addloanpremium'),
    url(r'^profile/$',views.profile,name='profile'),
    url(r'^editprofile/$', views.editprofile, name='editprofile'),
    url(r'^update/(?P<ex_id>\d+)$',views.update,name='update'),
    url(r'^lptransaction/$', views.transactions, name='trans'),
    url(r'^lpfilter/$', views.lpfilter, name='lpfilter'),
    url(r'^chart2/$',views.getExpense2,name='getExpense2'),
    url(r'^loan_form/$',views.loan_form,name='loan_form'),
    url(r'^delete_user/(?P<u_id>\d+)$', views.delete_user, name='delete_user'),
    url(r'^pdf',views.pdf,name="pdf"),

]