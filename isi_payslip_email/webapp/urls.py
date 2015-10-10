
from django.conf.urls import patterns, include, url

from .views import HomeView

urlpatterns = patterns('',
                url(r'^$', HomeView.as_view(), name='home'),
                url(r'^login/$', 'django.contrib.auth.views.login'),
                url(r'^logout/$', 'django.contrib.auth.views.logout'),
            )