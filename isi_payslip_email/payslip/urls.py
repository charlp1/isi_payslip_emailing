from __future__ import absolute_import
from django.conf.urls import include, url, patterns

from .views import Home, EmployeeView, PayslipSendView, PayslipUploadView

urlpatterns = patterns("",
                       url(r'^$', Home.as_view(), name='home'),
                       url(r'^employee/$', EmployeeView.as_view(), name='employee'),
                       url(r"send/?$", PayslipSendView.as_view(), name="send-payslip"),
                       url(r"upload/?$", PayslipUploadView.as_view(), name="upload-payslip")
                       )