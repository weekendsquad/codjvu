import uuid

from django.db import transaction, IntegrityError
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticated
from custom_auth.decorators import enforce_csrf
from .models import Tag, Snippet, SnippetTag, Url
from .serializers import TagSerializer, TagReadSerializer, SnippetSerializer, SnippetTagSerializer, \
    SnippetTagSerializerRead, SnippetUrlSerializer, SnippetUrlReadSerializer, SnippetSerializerRead

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


def create_list_of_object(snippet_id, items, key):
    snippet_integrated_data = []
    for item in items:
        data = {
            key: item,
            'snippet': snippet_id
        }
        snippet_integrated_data.append(data)
    return snippet_integrated_data


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@enforce_csrf
def tag_view(request):
    data = request.data

    data['user_id'] = request.user.id
    serializer = TagSerializer(data=data)
    if serializer.is_valid():
        if not request.user.is_system_admin:
            if not check_tag_limit(request.user.id, request.user.is_system_admin,
                                   request.user.is_pro, request.user.is_trial):
                return JsonResponse(serializer.errors, status=403)
        serializer.save()
        return JsonResponse(serializer.data, status=201)
    return JsonResponse(serializer.errors, status=400)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
@csrf_exempt
def tag_list_public_view(request):
    public_tags_serializer = TagReadSerializer(Tag.objects.filter(user_id__is_system_admin__contains="true"), many=True)
    return JsonResponse(public_tags_serializer.data, status=200, safe=False)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
@csrf_exempt
def tag_list_private_view(request):
    private_tags_serializer = TagReadSerializer(Tag.objects.filter(user_id=request.user.id), many=True)
    return JsonResponse(private_tags_serializer.data, status=200, safe=False)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
@enforce_csrf
def tag_update_view(request):
    data = JSONParser().parse(request)
    data["user_id"] = request.user.id
    try:
        tag = Tag.objects.get(id=data["id"], user_id=request.user.id)
    except Tag.DoesNotExist:
        return HttpResponse(status=404)

    serializer = TagSerializer(tag, data=data)
    if serializer.is_valid():
        serializer.save()
        return JsonResponse(serializer.data)
    return JsonResponse(serializer.errors, status=400)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
@enforce_csrf
def tag_delete_view(request):
    data = JSONParser().parse(request)
    try:
        tag = Tag.objects.get(id=data["id"], user_id=request.user.id)
    except Tag.DoesNotExist:
        return HttpResponse(status=404)
    tag.delete()
    return HttpResponse(status=204)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@enforce_csrf
@transaction.atomic
def snippet_view(request):
    tag_id = request.data['tag_id']
    urls = request.data['url']

    snippet_data = {
        'user': request.user.id,
        'snippet': request.data['snippet'],
        'language': request.data['language_id']
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

    snippet_url_data = create_list_of_object(snippet_serializer.data['id'], urls, 'url')
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


@api_view(['GET'])
@permission_classes([IsAuthenticated])
@csrf_exempt
def snippet_list_view(request):
    snippet_serializer = SnippetSerializerRead(Snippet.objects.filter(user=request.user).all(), many=True)
    return JsonResponse(snippet_serializer.data, status=200, safe=False)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
@csrf_exempt
def snippet_details_view(request, snippet_id):
    data = {}
    try:
        snippet_serializer = SnippetSerializer(Snippet.objects.get(id=snippet_id, user=request.user))
    except Snippet.DoesNotExist:
        return HttpResponse(status=404)
    else:
        data["snippet"] = snippet_serializer.data
    try:
        snippet_tag_serializer = SnippetTagSerializerRead(SnippetTag.objects.filter(snippet=snippet_id).all(), many=True)
    except Tag.DoesNotExist:
        data["tag"] = []
    else:
        data["tag"] = snippet_tag_serializer.data
    try:
        snippet_url_serializer = SnippetUrlReadSerializer(Url.objects.filter(snippet=snippet_id).all(), many=True)
    except Url.DoesNotExist:
        data["url"] = []
    else:
        data["url"] = snippet_url_serializer.data
    return JsonResponse(data, status=200, safe=False)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
@enforce_csrf
def snippet_delete_view(request):
    data = JSONParser().parse(request)
    try:
        snippet = Snippet.objects.get(id=data["id"], user=request.user)
    except Snippet.DoesNotExist:
        return HttpResponse(status=404)
    snippet.delete()
    return HttpResponse(status=204)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
@enforce_csrf
@enforce_csrf
@transaction.atomic
def snippet_update_view(request):
    data = JSONParser().parse(request)
    snippet_data = {
        'user': request.user.id,
        'snippet': data['snippet'],
        'language': data['language_id']
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

            snippet_tag_data = create_list_of_object(data['id'], data['tag_id'], 'tag')
            snippet_tag_serializer = SnippetTagSerializer(data=snippet_tag_data, many=True)

            snippet_url_data = create_list_of_object(data['id'], data['url'], 'url')
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
