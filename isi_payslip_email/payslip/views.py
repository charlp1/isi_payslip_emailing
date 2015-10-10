from __future__ import absolute_import
from django.core.exceptions import ObjectDoesNotExist
from django.views.generic import TemplateView


class PayslipSendView(TemplateView):
    template_name = 'payslip/index.html'








