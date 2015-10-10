from __future__ import absolute_import


from os.path import join
from datetime import date, timedelta
from django.core.exceptions import ObjectDoesNotExist
from django.views.generic import TemplateView, View
from django.views.decorators.csrf import csrf_exempt

from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.shortcuts import redirect
from django.views.generic import FormView, TemplateView
from django.conf import settings
from django.http import JsonResponse

from .forms import SendPayslipForm
from .models import Employee, Payslip


class Home(TemplateView):
    template_name = 'home.html'

class EmployeeView(TemplateView):
    template_name = 'employee_table.html'

    def get_context_data(self, **kwargs):
        context = super(EmployeeView, self).get_context_data(**kwargs)
        context['table'] = True

        make_emp = lambda u: {'id':u.id, 'name': u.name, 'email': u.email,
                               'active': u.active, 'send_email': u.send_email,
                               'cc_email': u.cc_email}

        if(self.request.GET.get('id')):
            id = int(self.request.GET.get('id'))
            pslips = Payslip.objects.filter(employee=id)
            context['payslips'] = []
            for p in pslips:
                context['payslips'].append({'name': p.filename.name, 'date': p.date_release})

            context['emp'] = {'name' : p.employee.name, 'email' : p.employee.email, 'active' : p.employee.active}
            context['table'] = False
        else:
            emp = Employee.objects.all()

            context['emp'] = [ make_emp(e) for e in emp ]

        return context




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
        data = request.FILES['files[]']

        date_today = date.today()
        today = date_today.strftime('%d')

        f_day = get_first_day(date_today)
        f = 16 if int(today) > 15 else f_day.strftime('%d')

        l_day = get_last_day(date_today)
        l = l_day.strftime('%d') if int(today) > 15 else 15
        pay_folder = "{0}-{1}-{2}".format(date_today.strftime('%Y-%m'), f, l)
        path = default_storage.save(join(settings.MEDIA_ROOT, pay_folder, data.name), ContentFile(data.read()))


        return JsonResponse({'status': 'ok'})


def get_first_day(dt, d_years=0, d_months=0):
    # d_years, d_months are "deltas" to apply to dt
    y, m = dt.year + d_years, dt.month + d_months
    a, m = divmod(m-1, 12)
    return date(y+a, m+1, 1)


def get_last_day(dt):
    return get_first_day(dt, 0, 1) + timedelta(-1)
