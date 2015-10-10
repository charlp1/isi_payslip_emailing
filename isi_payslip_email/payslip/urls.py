from __future__ import absolute_import
from django.conf.urls import include, url, patterns

from .views import PayslipSendView, PayslipUploadView

urlpatterns = patterns("",
                       url(r"send/?$", PayslipSendView.as_view(), name="send-payslip"),
                       url(r"upload/?$", PayslipUploadView.as_view(), name="upload-payslip")
                       )