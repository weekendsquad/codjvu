import jwt
from rest_framework.authentication import BaseAuthentication
from rest_framework import exceptions
from django.conf import settings
from django.contrib.auth import get_user_model


class JWTAuthentication(BaseAuthentication):

    def authenticate(self, request):
        User = get_user_model()
        # authorization_header = request.headers.get('Authorization')  # token in http header
        authorization_header = request.META.get('HTTP_AUTHORIZATION')  # Get from Bearer token
        if authorization_header is not None:
            access_token = authorization_header.split(' ')[1]

            if access_token == 'null':
                return None
            try:
                # access_token = authorization_header.split(' ')[1]
                payload = jwt.decode(
                    access_token, settings.SECRET_KEY, algorithms=['HS256'])
            except jwt.ExpiredSignatureError:
                raise exceptions.AuthenticationFailed('access_token expired')
            except IndexError:
                raise exceptions.AuthenticationFailed('Token prefix missing')

            user = User.objects.filter(id=payload['id']).first()
            if user is None:
                raise exceptions.AuthenticationFailed('User not found')

            if not user.is_active:
                raise exceptions.AuthenticationFailed('user is inactive')
            return user, None
        else:
            return None

