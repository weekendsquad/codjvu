from datetime import datetime

from django.contrib.auth import get_user_model
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import ensure_csrf_cookie
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import exceptions
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.serializers import TokenRefreshSerializer, TokenBlacklistSerializer
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
    headers = {
        "access_token": token["access"],
        "refresh_token": token["refresh"]
    }
    data = {
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


@api_view(['POST'])
@permission_classes([AllowAny])
def token_refresh_view(request):
    serializer = TokenRefreshSerializer(data=request.data)
    try:
        serializer.is_valid(raise_exception=True)
    except TokenError as e:
        return JsonResponse(e, status=400)
    response = JsonResponse(data={}, status=200)
    response['access_token'] = serializer.validated_data['access']
    response['refresh_token'] = serializer.validated_data['refresh']
    return response


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def token_blacklist_view(request):
    serializer = TokenBlacklistSerializer(data=request.data)
    try:
        serializer.is_valid(raise_exception=True)
    except TokenError as e:
        return JsonResponse(e, status=400)
    return HttpResponse(status=200)