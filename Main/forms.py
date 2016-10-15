from django.contrib.auth.models import User
from django import forms
from django.utils.translation import ugettext_lazy as _

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username','first_name','last_name', 'email', 'password']


class Expform(forms.ModelForm):
    paid_to=forms.RegexField(regex='^\w+$',widget=forms.TextInput(attrs=dict(required=True, max_length=30)),
                             label=_("paid_to"),
                             error_message={'invalid':_("This field only contains letters, numbers or underscore.")})\
