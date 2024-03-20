import uuid

from django.db import transaction, IntegrityError
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticated
from custom_auth.decorators import enforce_csrf
from django.views.decorators.csrf import ensure_csrf_cookie
from .models import Tag, Snippet, SnippetTag, Url, Language
from .serializers import TagSerializer, TagReadSerializer, SnippetSerializer, SnippetTagSerializer, \
    SnippetUrlSerializer, SnippetUrlReadSerializer, SnippetReadSerializer, LanguageSerializer, \
    SnippetTagReadSerializer

TAGS_LIMIT = 5


def check_tag_limit(user_id, is_sys_admin, is_pro, is_trial):
    number_of_tags = Tag.objects.filter(user_id=user_id).count()
    if is_trial or is_pro:
        if number_of_tags > 20:  # TODO: Get these value from the admin table
            return False
        else:
            return True
    elif is_sys_admin:
        return True
    else:
        if number_of_tags > 5:  # TODO: Get these value from the admin table
            return False
        else:
            return True


def create_list_of_object(snippet_id, items, key, user=None):
    snippet_integrated_data = []
    for item in items:
        if user:
            data = {
                key: item,
                'snippet': snippet_id,
                'user': user
            }
        else:
            data = {
                key: item,
                'snippet': snippet_id,
            }
        snippet_integrated_data.append(data)
    return snippet_integrated_data


@api_view(['GET', 'POST', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def tag_view(request):
    if request.method == 'POST':
        return create_tag(request)
    elif request.method == 'GET':
        return read_tag(request)
    elif request.method == 'DELETE':
        return delete_tag(request)
    elif request.method == 'PUT':
        return update_tag(request)


@csrf_exempt
def create_tag(request):
    data = request.data
    data['user'] = request.user.id
    serializer = TagSerializer(data=data)
    if serializer.is_valid():
        if not request.user.is_system_admin:
            if not check_tag_limit(request.user.id, request.user.is_system_admin,
                                   request.user.is_pro, request.user.is_trial):
                return JsonResponse(serializer.errors, status=403)
        serializer.save()
        return JsonResponse(serializer.data, status=201)
    return JsonResponse(serializer.errors, status=400)


@csrf_exempt
def read_tag(request):
    data = {}
    public_tag_data = get_public_tag(request)
    private_tag_data = get_private_tag(request)
    data['private'] = private_tag_data
    data['public'] = public_tag_data
    return JsonResponse(data, status=200, safe=False)


def get_public_tag(request):
    public_tags_serializer = TagReadSerializer(Tag.objects.filter(user_id__is_system_admin__contains="true"), many=True)
    return public_tags_serializer.data


def get_private_tag(request):
    private_tags_serializer = TagReadSerializer(Tag.objects.filter(user=request.user), many=True)
    return private_tags_serializer.data


@csrf_exempt
def update_tag(request):
    data = JSONParser().parse(request)
    data["user"] = request.user.id
    try:
        tag = Tag.objects.get(id=data["id"], user=request.user)
    except Tag.DoesNotExist:
        return HttpResponse(status=404)

    serializer = TagSerializer(tag, data=data)
    if serializer.is_valid():
        serializer.save()
        return JsonResponse(serializer.data)
    return JsonResponse(serializer.errors, status=400)


@csrf_exempt
def delete_tag(request):
    data = JSONParser().parse(request)
    try:
        tag = Tag.objects.filter(id__in=data["id"], user=request.user)
    except Tag.DoesNotExist:
        return HttpResponse(status=404)
    tag.delete()
    return HttpResponse(status=204)


@api_view(['GET', 'POST', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def snippet_view(request, snippet_id=None):
    if request.method == 'POST':
        return create_snippet(request)
    elif request.method == 'GET':
        return read_snippet(request, snippet_id)
    elif request.method == 'DELETE':
        return delete_snippet(request)
    elif request.method == 'PUT':
        return update_snippet(request)


@csrf_exempt
@transaction.atomic
def create_snippet(request):
    tag_id = request.data['tag_info']
    urls = request.data['url_info']
    snippet_data = {
        'user': request.user.id,
        'title': request.data['title'],
        'snippet': request.data['snippet'],
        'language': request.data['language']
    }
    try:
        with transaction.atomic():
            snippet_serializer = SnippetSerializer(data=snippet_data)
            if snippet_serializer.is_valid():
                snippet_serializer.save()
            else:
                return JsonResponse(snippet_serializer.errors, status=400, safe=False)
    except IntegrityError as error:
        return JsonResponse(snippet_serializer.errors, status=400)

    snippet_tag_data = create_list_of_object(snippet_serializer.data['id'], tag_id, 'tag')
    snippet_tag_serializer = SnippetTagSerializer(data=snippet_tag_data, many=True)

    snippet_url_data = create_list_of_object(snippet_serializer.data['id'], urls, 'url', request.user.id)
    snippet_url_serializer = SnippetUrlSerializer(data=snippet_url_data, many=True)

    if snippet_tag_serializer.is_valid():
        snippet_tag_serializer.save()
    else:
        return JsonResponse(snippet_tag_serializer.errors, status=400, safe=False)

    if snippet_url_serializer.is_valid():
        snippet_url_serializer.save()
    else:
        return JsonResponse(snippet_url_serializer.errors, status=400, safe=False)

    return HttpResponse(status=201)


@csrf_exempt
def read_snippet(request, snippet_id=None):
    if snippet_id:
        data = {}
        try:
            snippet_serializer = SnippetSerializer(Snippet.objects.get(id=snippet_id, user=request.user))
        except Snippet.DoesNotExist:
            return HttpResponse(status=404)
        else:
            data = snippet_serializer.data
        try:
            snippet_tag_serializer = SnippetTagReadSerializer(SnippetTag.objects.filter(snippet=snippet_id).all(),
                                                              many=True)
        except Tag.DoesNotExist:
            data["tag_info"] = []
        else:
            data["tag_info"] = [d["tag"] for d in snippet_tag_serializer.data]
        try:
            snippet_url_serializer = SnippetUrlReadSerializer(Url.objects.filter(snippet=snippet_id).all(),
                                                              many=True)
        except Url.DoesNotExist:
            data["url_info"] = []
        else:
            data["url_info"] = snippet_url_serializer.data
        return JsonResponse(data, status=200, safe=False)
    else:
        snippet_serializer = SnippetReadSerializer(Snippet.objects.filter(user=request.user).all(), many=True)
        return JsonResponse(snippet_serializer.data, status=200, safe=False)


@csrf_exempt
def delete_snippet(request):
    data = JSONParser().parse(request)
    try:
        snippet = Snippet.objects.filter(id__in=data["id"], user=request.user)
    except Snippet.DoesNotExist:
        return HttpResponse(status=404)
    snippet.delete()
    return HttpResponse(status=204)


@csrf_exempt
@transaction.atomic
def update_snippet(request):
    data = JSONParser().parse(request)
    snippet_data = {
        'user': request.user.id,
        'title': data['title'],
        'snippet': data['snippet'],
        'language': data['language']
    }
    try:
        with transaction.atomic():
            snippet = Snippet.objects.get(id=data['id'], user=request.user)
            serializer = SnippetSerializer(snippet, data=snippet_data)
            if serializer.is_valid():
                serializer.save()

            snippet_tag = SnippetTag.objects.filter(snippet=data['id']).all()
            if snippet_tag:
                snippet_tag.delete()

            snippet_url = Url.objects.filter(snippet=data['id'], user=request.user).all()
            if snippet_url:
                snippet_url.delete()

            snippet_tag_data = create_list_of_object(data['id'], data['tag_info'], 'tag')
            snippet_tag_serializer = SnippetTagSerializer(data=snippet_tag_data, many=True)

            snippet_url_data = create_list_of_object(data['id'], data['url_info'], 'url', request.user.id)
            snippet_url_serializer = SnippetUrlSerializer(data=snippet_url_data, many=True)

            if snippet_tag_serializer.is_valid():
                snippet_tag_serializer.save()
            else:
                return JsonResponse(snippet_tag_serializer.errors, status=400, safe=False)
            if snippet_url_serializer.is_valid():
                snippet_url_serializer.save()
            else:
                return JsonResponse(snippet_url_serializer.errors, status=400, safe=False)
    except Snippet.DoesNotExist:
        return HttpResponse(status=404)
    except IntegrityError as error:
        return JsonResponse(serializer.errors, status=400)
    return HttpResponse(status=201)


@csrf_exempt
def read_language(request):
    languages = Language.objects.all()
    serializer = LanguageSerializer(languages, many=True)
    return JsonResponse(serializer.data, safe=False)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def language_view(request):
    if request.method == 'GET':
        return read_language(request)
