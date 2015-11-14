from __future__ import absolute_import
from django.conf.urls import include, url, patterns


from .views import (Home, EmployeeView, PayslipSendView, PayslipUploadView,
                    MissingUploadedEmployeeAPIView, EmployeeProfile)

urlpatterns = patterns("",
                       url(r'^$', Home.as_view(), name='home'),
                       url(r'^employee/$', EmployeeView.as_view(), name='employee'),
                       url(r'employee/id(/(?P<id>(\d+)))?/?', EmployeeProfile.as_view(), name='employee_profile'),
                       url(r"^send/?$", PayslipSendView.as_view(), name="send-payslip"),
                       url(r"^upload/?$", PayslipUploadView.as_view(), name="upload-payslip")
                       )

urlpatterns += patterns('',
                        url(r"^api/missing_employee/$", MissingUploadedEmployeeAPIView.as_view(),
                            name='missing_employees'),
                        )
