from rest_framework import serializers
from snippet.models import Tag


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'tag', 'user_id']
        read_only_fields = ('id',)
