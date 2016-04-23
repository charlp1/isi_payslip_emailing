from __future__ import absolute_import
from django.conf.urls import include, url, patterns


from .views import (Home, EmployeeView, PayslipSendView, PayslipUploadView,
                    MissingUploadedEmployeeAPIView, EmployeeProfile, PayslipSendAPIView,
                    FolderContent, LogUploadedSendPayslipAPIView, LogUploadedSendPayslipView,
                    SearchPayslipAPIView)

urlpatterns = patterns("",
                       url(r'^$', Home.as_view(), name='home'),
                       url(r'^employee/$', EmployeeView.as_view(), name='employee'),
                       url(r'employee/id(/(?P<id>(\d+)))?/?', EmployeeProfile.as_view(), name='employee_profile'),
                       url(r'folder/content/$', FolderContent.as_view(), name='folder_content'),
                       url(r"^send/?$", PayslipSendView.as_view(), name="send-payslip"),
                       url(r"^upload/?$", PayslipUploadView.as_view(), name="upload-payslip")
                       )
# api
urlpatterns += patterns('',
                        url(r"^api/search/$", SearchPayslipAPIView.as_view(),
                            name='search_payslip'),
                        url(r"^api/missing_employee/$", MissingUploadedEmployeeAPIView.as_view(),
                            name='missing_employees'),
                        url(r"^api/send/$", PayslipSendAPIView.as_view(),
                            name='send_email_payslip'),
                        url(r"^api/logs/upload_sent/$", LogUploadedSendPayslipAPIView.as_view(),
                            name='logs_upload_sent_api'),
                        )
# logs
urlpatterns += patterns('',
                        url(r"^logs/upload_sent/$", LogUploadedSendPayslipView.as_view(),
                            name='logs_upload_sent'),
                        url(r"^logs/upload_sent/export/?$", LogUploadedSendPayslipAPIView.as_view(),
                            name='logs_upload_sent_export')
                        )
