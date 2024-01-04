import jwt
from rest_framework.authentication import BaseAuthentication
from django.middleware.csrf import CsrfViewMiddleware
from rest_framework import exceptions
from django.conf import settings
from django.contrib.auth import get_user_model


class CSRFCheck(CsrfViewMiddleware):
    def _reject(self, request, reason):
        return reason


def enforce_csrf(request):
    check = CSRFCheck(request.META.get('HTTP_X_CSRFTOKEN'))
    check.process_request(request)
    reason = check.process_view(request, None, (), {})
    print(reason)
    if reason:
        raise exceptions.PermissionDenied('CSRF Failed: %s' % reason)


class JWTAuthentication(BaseAuthentication):

    def authenticate(self, request):

        User = get_user_model()
        authorization_header = request.headers.get('Authorization')
        if not authorization_header:
            return None
        try:
            # access_token = authorization_header.split(' ')[1]
            access_token = authorization_header
            payload = jwt.decode(
                access_token, settings.SECRET_KEY, algorithms=['HS256'])
            print(payload)
        except jwt.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed('access_token expired')
        except IndexError:
            raise exceptions.AuthenticationFailed('Token prefix missing')

        user = User.objects.filter(id=payload['id']).first()
        if user is None:
            raise exceptions.AuthenticationFailed('User not found')

        if not user.is_active:
            raise exceptions.AuthenticationFailed('user is inactive')

        enforce_csrf(request)
        return user, None
