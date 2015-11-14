from __future__ import absolute_import

import re
from os.path import join
from datetime import date, timedelta
from datetime import datetime
from django.core.exceptions import ObjectDoesNotExist
from django.views.generic import TemplateView, View
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.shortcuts import redirect
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.views.generic import FormView, TemplateView, ListView
from django.conf import settings
from django.http import JsonResponse, HttpResponse

from utils.api import GenericAPIView
from utils.export import exportDataAsExcelFile
from .forms import SendPayslipForm
from .models import Employee, Payslip, PayslipFolder


class Home(TemplateView):
    template_name = 'home.html'


class EmployeeView(TemplateView):
    template_name = 'employee/table.html'

    def get_context_data(self, **kwargs):
        context = super(EmployeeView, self).get_context_data(**kwargs)
        context['table'] = True

        make_emp = lambda u: {'id':u.id, 'name': u.name, 'email': u.email,
                               'active': u.active, 'send_email': u.send_email,
                               'cc_email': u.cc_email}


        emp = Employee.objects.all()
        context['emp'] = [ make_emp(e) for e in emp ]

        return context

class EmployeeProfile(TemplateView):
    template_name = 'employee/profile.html'

    def get_context_data(self, id, **kwargs):
        context = super(EmployeeProfile, self).get_context_data(**kwargs)
        emp = Employee.objects.get(id=id)
        pslips = Payslip.objects.filter(employee=id)
        context['payslips'] = []
        if pslips:
            for p in pslips:
                context['payslips'].append({'name': p.filename.name, 'date': p.date_release, 'id': p.pk,
                                            'created': p.created })

        context['emp'] = {'name' : emp.name, 'email' : emp.email, 'active' : emp.active}
        return context


class PayslipSendView(FormView):
    template_name = 'payslip/index.html'
    template_name_sent = 'payslip/success_email_payslip.html'
    form_class = SendPayslipForm
    success_url = 'payslip/send/'


class FolderContent(GenericAPIView):
    def post(self, request, **kwargs):
        id = int(request.POST.get('id'))
        pslips = Payslip.objects.filter(payslip_folder_id=id)
        data = []
        if pslips:
            for p in pslips:
                user = {
                    'payslip_id': p.pk,
                    'name': p.employee.name,
                    'email': p.employee.email,
                    'filename': p.filename.name,
                    'active': p.employee.active,
                    'send_email': p.employee.send_email
                }
                data.append(user)

        return JsonResponse(data=data, safe=False)

class PayslipUploadView(TemplateView):
    template_name = 'payslip/upload.html'

    def post(self, request):
        data = request.FILES['files[]']

        filename = data.name
        split_name = filename.split(settings.PAYSLIP_PATH_SEPARATOR)

        response = {
            'status': 'error',
            'filename': filename,
            'message': ''
        }
        check = True
        if not filename.endswith('.pdf'):
            check = False
            response.update({'message': 'Invalid File Format.'})

        if len(split_name) != 2:
            check = False
            response.update({'message': 'Invalid Filename Format.'})

        if check:
            pf_name = split_name[0].strip()
            e_name = re.sub('.pdf', '', split_name[1]).strip()

            try:
                employee = Employee.objects.get(name=e_name)
            except Employee.DoesNotExist:
                response.update({'message': 'No Employee Found.'})
            else:
                payslip_folder, created = PayslipFolder.objects.get_or_create(name=pf_name)

                precord = {'employee': employee, 'filename': data, 'payslip_folder': payslip_folder, 'status':False}
                payslip, p_created = Payslip.objects.update_or_create(employee=employee, payslip_folder=payslip_folder,
                                                                      defaults=precord)
                if p_created:
                    payslip_folder.total_uploaded = Payslip.objects.filter(payslip_folder=payslip_folder).count()
                payslip_folder.status = False
                payslip_folder.save()
                response.update({'status': 'ok', 'message': 'success'})

        return JsonResponse(response)


class MissingUploadedEmployeeAPIView(GenericAPIView):

    allowed_methods = ['GET', ]

    def get(self, request, *args, **kwargs):
        response = {
            'status': 'error',
            'message': 'Request Invalid.',
            'data': {}
        }
        data = request.query_params
        pf_name = data.get('payslip', None)
        if pf_name:
            try:
                payslip_folder = PayslipFolder.objects.get(name=pf_name)
            except PayslipFolder.DoesNotExist:
                response.update({'message': 'No Payslip Found.'})
            else:
                employee_ids = Payslip.objects.values_list('employee_id').filter(payslip_folder=payslip_folder)
                employees = Employee.objects.filter(active=True, send_email=True).exclude(pk__in=employee_ids)
                response.update({'status': 'ok', 'message': 'success', 'data': [e.name for e in employees]})

        return JsonResponse(response)


class PayslipSendAPIView(GenericAPIView):
    allowed_methods = ['POST']

    def post(self, request, *args, **kwargs):
        response = {
            'status': 'error',
            'message': 'Request Invalid',
            'data': {}
        }
        data = request.data
        pid = data.get('pid', None)
        try:
            payslip = Payslip.objects.get(pk=pid)
        except Payslip.DoesNotExist:
            response.update({'message': 'No Payslip Record Found.'})
        else:
            body_message = render_to_string('payslip/send_payslip_message.html', {'employee_name': payslip.employee.name,
                                                                                  'duration': payslip.payslip_folder.name})
            email = EmailMultiAlternatives(subject='Payslip {}'.format(payslip.payslip_folder.name), body=body_message,
                                           from_email=settings.COMPANY_EMAIL, to=[payslip.employee.email],
                                           bcc=[payslip.employee.cc_email])
            payslip_employee_pdf = join(settings.MEDIA_ROOT, payslip.filename.path)
            email.attach_file(payslip_employee_pdf, 'application/pdf')
            email.attach_alternative(body_message, 'text/html')
            if email.send(fail_silently=False):
                payslip.date_release = datetime.now()
                payslip.status = True
                payslip.save()

                total_sent = Payslip.objects.filter(status=True, payslip_folder=payslip.payslip_folder).count()
                payslip.payslip_folder.total_sent = total_sent
                if total_sent >= payslip.payslip_folder.total_uploaded:
                    payslip.payslip_folder.status = True
                payslip.payslip_folder.save()

                response.update({'status': 'ok', 'message': 'success',
                                 'data': {'id': pid, 'date_release': payslip.date_release}})
            else:
                response.update({'message': "Unable to send email for employee {} Payslip {}.".format(
                    payslip.employee.name, payslip.payslip_folder.name)})

        return JsonResponse(response)


class LogUploadedSendPayslipView(ListView):
    model = PayslipFolder
    template_name = 'payslip/logs_update_sent.html'
    context_object_name = 'payslip_folders'


class LogUploadedSendPayslipAPIView(GenericAPIView):

    def post(self, request, **kwargs):
        pid = request.data.get('pid', None)
        res = self.get_response_payslip(pid)
        return JsonResponse(data=res, safe=False)

    def get(self, request, **kwargs):
        pid = request.query_params.get('pid', None)
        res = self.get_response_payslip(pid)
        payslip = PayslipFolder.objects.get(pk=pid)
        header = [
            ('name', 'Employee Name'),
            ('email', 'Email'),
            ('filename', 'Filename'),
            ('active', 'Active'),
        ]
        sheets = [
            {'name': 'Payslip Uploaded', 'header': header, 'data': res['payslip_uploaded']},
            {'name': 'Payslip Sent', 'header': header, 'data': res['payslip_sent']},
            {'name': 'Payslip Unsent', 'header': header, 'data': res['payslip_unsent']},
        ]
        return exportDataAsExcelFile('{}_logs'.format(payslip.name), sheets)

    def get_response_payslip(self, pid):
        payslips = Payslip.objects.filter(payslip_folder_id=pid)
        uploaded = []
        sent = []
        unsent = []
        for p in payslips:
            user = {
                'payslip_id': p.pk,
                'name': p.employee.name,
                'email': p.employee.email,
                'filename': p.filename.name,
                'active': p.employee.active,
                'send_email': p.employee.send_email
            }
            if p.status:
                sent.append(user)
            else:
                unsent.append(user)
            uploaded.append(user)

        res = {
            'payslip_uploaded': uploaded,
            'payslip_sent': sent,
            'payslip_unsent': unsent
        }
        return res


def get_first_day(dt, d_years=0, d_months=0):
    # d_years, d_months are "deltas" to apply to dt
    y, m = dt.year + d_years, dt.month + d_months
    a, m = divmod(m-1, 12)
    return date(y+a, m+1, 1)


def get_last_day(dt):
    return get_first_day(dt, 0, 1) + timedelta(-1)
