from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes
from rest_framework.parsers import JSONParser
from manager.const import *
from custom_auth.decorators import enforce_csrf
from snippet.serializers import TagSerializer, LanguageSerializer
from .serializers import SettingSerializer
from rest_framework import permissions
from snippet.models import Language, Tag
from .models import Setting


class IsSystemAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_system_admin)


@csrf_exempt
def add_language(request):
    data = request.data
    serializer = LanguageSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return JsonResponse(serializer.data, status=201)
    return JsonResponse(serializer.errors, status=400)


@csrf_exempt
def delete_language(request):
    data = JSONParser().parse(request)
    try:
        language = Language.objects.get(pk=data["id"])
    except Language.DoesNotExist:
        return HttpResponse(status=404)

    language.delete()
    return HttpResponse(status=204)


@csrf_exempt
def update_language(request):
    data = JSONParser().parse(request)
    try:
        language = Language.objects.get(pk=data["id"])
    except Language.DoesNotExist:
        return HttpResponse(status=404)

    serializer = LanguageSerializer(language, data=data)
    if serializer.is_valid():
        serializer.save()
        return JsonResponse(serializer.data)
    return JsonResponse(serializer.errors, status=400)


@api_view(['POST', 'PUT', 'DELETE'])
@permission_classes([IsSystemAdmin])
def language_view(request):
    if request.method == 'POST':
        return add_language(request)
    elif request.method == 'DELETE':
        return delete_language(request)
    elif request.method == 'PUT':
        return update_language(request)


@api_view(['GET'])
@permission_classes([IsSystemAdmin])
@csrf_exempt
def tag_list_view(request):
    tags_serializer = TagSerializer(Tag.objects.all(), many=True)
    return JsonResponse(tags_serializer.data, status=200, safe=False)


@csrf_exempt
def read_tag_limit(request):
    setting = Setting.objects.get(key=TAG_LIMIT)
    serializer = SettingSerializer(setting)
    return JsonResponse(serializer.data)


@csrf_exempt
def update_tag_limit(request):
    data = JSONParser().parse(request)
    try:
        setting_tag_limit = Setting.objects.filter(key=TAG_LIMIT).get()
    except Setting.DoesNotExist:
        return HttpResponse(status=404)

    serializer = SettingSerializer(setting_tag_limit, data=data)
    if serializer.is_valid():
        serializer.save()
        return JsonResponse(serializer.data)
    return JsonResponse(serializer.errors, status=400)


@api_view(['GET', 'PUT'])
@permission_classes([IsSystemAdmin])
def setting_tag_limit_view(request):
    if request.method == 'GET':
        return read_tag_limit(request)
    elif request.method == 'PUT':
        return update_tag_limit(request)
