
from django.conf.urls import patterns, include, url

from .views import HomeView, Employee

urlpatterns = patterns('',
                        url(r'^$', HomeView.as_view(), name='home'),
                        url(r'^login/$', 'django.contrib.auth.views.login'),
                        url(r'^logout/$', 'django.contrib.auth.views.logout'),
                       url(r'^employees/$', Employee.as_view(), name='employee')
            )