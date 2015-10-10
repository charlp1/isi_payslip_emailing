from django.contrib.auth.decorators import login_required
from django.views.generic import ListView
from django.utils.decorators import method_decorator

from django.contrib.auth.models import User

class LoggedInMixin(object):
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(LoggedInMixin, self).dispatch(request, *args, **kwargs)

class HomeView(LoggedInMixin, ListView):
    template_name = 'home.html'

    def get_queryset(self):
        return User.objects.get(pk=1)
