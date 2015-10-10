from __future__ import absolute_import
from django.conf.urls import include, url, patterns

from .views import PayslipSendView

urlpatterns = patterns("",
                       url(r"send/?$", PayslipSendView.as_view(), name="send-payslip")
                       )