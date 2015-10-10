from __future__ import absolute_import
from django.core.exceptions import ObjectDoesNotExist
from django.views.generic import TemplateView


class PayslipSendView(TemplateView):
    template_name = 'payslip/index.html'


class PayslipUploadView(TemplateView):
    template_name = 'payslip/upload.html'

    def post(self, request):
        print("post", request)

        return JSONResponse({})