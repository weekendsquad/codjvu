from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticated

from custom_auth.decorators import enforce_csrf
from .serializers import LanguageSerializer
from rest_framework import permissions
from snippet.models import Language


class IsSystemAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_system_admin)


@api_view(['POST'])
@permission_classes([IsSystemAdmin])
@enforce_csrf
def language_view(request):
    data = request.data
    serializer = LanguageSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return JsonResponse(serializer.data, status=201)
    return JsonResponse(serializer.errors, status=400)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
@csrf_exempt
def language_list_view(request):
    languages = Language.objects.all()
    serializer = LanguageSerializer(languages, many=True)
    return JsonResponse(serializer.data, safe=False)


@api_view(['PUT'])
@permission_classes([IsSystemAdmin])
@enforce_csrf
def language_update_view(request):
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


@api_view(['DELETE'])
@permission_classes([IsSystemAdmin])
@enforce_csrf
def language_delete_view(request):
    data = JSONParser().parse(request)
    try:
        language = Language.objects.get(pk=data["id"])
    except Language.DoesNotExist:
        return HttpResponse(status=404)

    language.delete()
    return HttpResponse(status=204)
