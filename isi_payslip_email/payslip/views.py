from __future__ import absolute_import

from django.shortcuts import redirect
from django.views.generic import FormView, TemplateView

from .forms import SendPayslipForm
from .models import Employee


class PayslipSendView(FormView):
    template_name = 'payslip/index.html'
    template_name_sent = 'payslip/success_email_payslip.html'
    form_class = SendPayslipForm
    success_url = 'payslip/send/'

    def form_valid(self, form):
        employees = Employee.objects.filter(active=True, send_email=True)
        for employee in employees:
            form.send_payslip(employee)

        response_kwargs = {
            "request": self.request,
            "template": self.template_name_sent,
            "context": self.get_context_data(form=form)
        }

        return self.response_class(**response_kwargs)


class PayslipUploadView(TemplateView):
    template_name = 'payslip/upload.html'

    def post(self, request):
        pass