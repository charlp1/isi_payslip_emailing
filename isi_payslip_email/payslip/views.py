from __future__ import absolute_import
from django.core.exceptions import ObjectDoesNotExist
from django.views.generic import TemplateView, View
from django.views.decorators.csrf import csrf_exempt

from .models import Employee

class Home(TemplateView):
    template_name = 'home.html'

class EmployeeView(TemplateView):
    template_name = 'employee_table.html'

    def get_context_data(self, **kwargs):
        context = super(EmployeeView, self).get_context_data(**kwargs)

        make_emp = lambda u: {'name': u.name, 'email': u.email,
                               'active': u.active, 'send_email': u.send_email,
                               'cc_email': u.cc_email}
        emp = Employee.objects.all()
        context['emp'] = [ make_emp(e) for e in emp ]
        return context


class PayslipSendView(TemplateView):
    template_name = 'payslip/index.html'


class PayslipUploadView(TemplateView):
    template_name = 'payslip/upload.html'

    def post(self, request):
        print("post", request)

        pass
