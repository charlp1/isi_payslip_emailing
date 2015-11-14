from __future__ import absolute_import

from rest_framework.views import APIView
from rest_framework.authentication import SessionAuthentication


class UnsafeSessionAuthentication(SessionAuthentication):

    def authenticate(self, request):
        http_request = request._request
        user = getattr(http_request, 'user', None)

        if not user or not user.is_active:
            return None

        return (user, None)


class GenericAPIView(APIView):

    # FIXME/TODO: For now we will just exempt everything
    authentication_classes = (UnsafeSessionAuthentication,)
    allowed_methods = ['GET', 'POST', 'PUT', 'DELETE']

    def __init__(self):
        super(GenericAPIView, self).__init__()
        self.user = None

    def dispatch(self, request, *args, **kwargs):
        self.user = request.user

        return super(GenericAPIView, self).dispatch(request, *args, **kwargs)
