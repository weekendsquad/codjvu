from functools import wraps

from django.core.handlers import exception
from django.middleware.csrf import CsrfViewMiddleware


class CSRFCheck(CsrfViewMiddleware):
    def _reject(self, request, reason):
        return reason


def enforce_csrf(function):
    @wraps(function)
    def wrap(request, *args, **kwargs):
        check = CSRFCheck(request.META.get('HTTP_X_CSRFTOKEN'))
        check.process_request(request)
        reason = check.process_view(request, None, (), {})
        print(reason)
        if reason:
            raise exception.PermissionDenied('CSRF Failed: %s' % reason)
        return function(request, *args, **kwargs)
    return wrap
