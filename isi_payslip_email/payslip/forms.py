from os import path
from django import forms
from django.conf import settings
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from datetime import datetime

from .models import Payslip

class SendPayslipForm(forms.Form):

    payslip_path = forms.CharField(label="Payslips")

    def clean_payslip_path(self):
        payslip_path = self.cleaned_data.get("payslip_path")
        if not payslip_path or not path.isdir(path.join(settings.MEDIA_ROOT, payslip_path)):
            raise forms.ValidationError("Payslips not available.")
        return self.cleaned_data["payslip_path"]

    def send_payslip(self, employee):
        payslip_path = self.cleaned_data['payslip_path']
        pdf_filename = "{} {} {}.pdf".format(payslip_path, settings.PAYSLIP_PATH_SEPARATOR, employee.name)
        payslip_employee_pdf = path.join(settings.MEDIA_ROOT, payslip_path, pdf_filename)

        if path.isfile(payslip_employee_pdf):
            body_message = render_to_string('payslip/send_payslip_message.txt', {'employee_name': employee.name})
            email = EmailMessage(subject='Employee Payslip', body=body_message, from_email=settings.COMPANY_EMAIL,
                                 to=[employee.email], bcc=[employee.cc_email])
            email.attach_file(payslip_employee_pdf, 'application/pdf')

            if email.send(fail_silently=False):
                precord = {'employee': employee, 'filename': pdf_filename, 'date_release': datetime.now()}
                Payslip(**precord).save()
            else:
                print "Unable to send email for employee {} Payslip {}.".format(employee.name, payslip_path)
        else:
            print "Employee {} Payslip not available for {} payslip.".format(employee.name, payslip_path)


