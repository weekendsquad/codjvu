from datetime import datetime

from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import exceptions
from .auth import generate_access_token
from .serializers import RegisterSerializer, LoginSerializer


@api_view(['POST'])
@permission_classes([AllowAny])
@ensure_csrf_cookie
def login_view(request):
    user_auth_model = get_user_model()
    email = request.data.get('email')
    password = request.data.get('password')
    if (email is None) or (password is None):
        raise exceptions.AuthenticationFailed(
            'email and password required')

    user = user_auth_model.objects.filter(email=email).first()
    if user is None:
        raise exceptions.AuthenticationFailed('user not found')
    if not user.check_password(password):
        raise exceptions.AuthenticationFailed('wrong password')
    token = generate_access_token(user)
    refresh_token = token["refresh"]

    headers = {
        "token": token["access"]
    }
    data = {
        "refresh_token": refresh_token,
        "last_login": datetime.now()
    }
    serializer = LoginSerializer(data=data)
    serializer.update(instance=user, validated_data=data)
    return Response(headers=headers)


@api_view(['POST'])
@permission_classes([AllowAny])
@ensure_csrf_cookie
def registration_view(request):
    data = request.data
    serializer = RegisterSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return JsonResponse(serializer.data, status=201)
    return JsonResponse(serializer.errors, status=400)
