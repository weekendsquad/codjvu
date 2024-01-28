from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from custom_auth.decorators import enforce_csrf
from .models import Tag
from .serializers import TagSerializer

TAGS_LIMIT = 5


def check_tag_limit(user_id):
    number_of_tags = Tag.objects.filter(user_id=user_id).count()
    if number_of_tags > 5:
        return False
    else:
        return True


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@enforce_csrf
def tag_view(request):
    data = request.data

    data['user_id'] = request.user.id
    serializer = TagSerializer(data=data)
    if serializer.is_valid():
        if not request.user.is_system_admin:
            if not check_tag_limit(request.user.id):
                return JsonResponse(serializer.errors, status=403)
        serializer.save()
        return JsonResponse(serializer.data, status=201)
    return JsonResponse(serializer.errors, status=400)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
@csrf_exempt
def tag_list_view(request):
    pass


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
@enforce_csrf
def tag_update_view(request):
    pass


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
@enforce_csrf
def tag_delete_view(request):
    return HttpResponse(status=204)
