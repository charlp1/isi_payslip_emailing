from __future__ import absolute_import

import json

from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView, View
from django.utils.decorators import method_decorator
from django.http import HttpResponse


class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders it's content into JSON.
    """
    def __init__(self, data, allowed_host='*', **kwargs):
        content = json.dumps(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)

class BASEAPIListView(View):
    http_method_names = ['get']

    def __init__(self, *args, **kwargs):
        self.response = JSONResponse

    def process_response(self, data, value=''):
        return self.response(data, value)

class LoggedInMixin(object):
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(LoggedInMixin, self).dispatch(request, *args, **kwargs)

class HomeView(LoggedInMixin, TemplateView):
    template_name = 'home.html'

class Employee(BASEAPIListView):
    def get(self):
        pass

