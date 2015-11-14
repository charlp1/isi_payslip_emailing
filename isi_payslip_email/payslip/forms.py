from os import path, listdir
from django import forms
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from datetime import datetime

from .models import Payslip, PayslipFolder

def get_payslip_choices():
    # you place some logic here
    payslip_folder = PayslipFolder.objects.filter(status=False)
    if payslip_folder:
        return [[p.id, p.name] for p in payslip_folder]

    return []


class SendPayslipForm(forms.Form):

    payslip_path = forms.ChoiceField(choices=get_payslip_choices())

    def __init__(self, *args, **kwargs):
        super(SendPayslipForm, self).__init__(*args, **kwargs)
        self.fields['payslip_path'] = forms.ChoiceField(
            choices=get_payslip_choices())