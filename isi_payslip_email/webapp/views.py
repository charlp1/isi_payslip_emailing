from __future__ import absolute_import

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView, View


class LoggedInMixin(object):
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(LoggedInMixin, self).dispatch(request, *args, **kwargs)

class HomeView(LoggedInMixin, TemplateView):
    template_name = 'home.html'

