from rest_framework import serializers
from snippet.models import Tag, Snippet, SnippetTag, Url


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'tag', 'user']
        read_only_fields = ('id',)


class TagReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'tag']
        read_only_fields = ('id',)


class SnippetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Snippet
        fields = ['id', 'user', 'snippet', 'language']
        read_only_fields = ('id',)


class SnippetSerializerRead(serializers.ModelSerializer):
    class Meta:
        model = Snippet
        fields = ['id', 'snippet', 'language']
        read_only_fields = ('id',)


class SnippetTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = SnippetTag
        fields = ['id', 'tag', 'snippet']
        read_only_fields = ('id',)


class SnippetTagSerializerRead(serializers.ModelSerializer):
    class Meta:
        model = SnippetTag
        fields = ['id', 'tag']


class SnippetUrlSerializer(serializers.ModelSerializer):
    class Meta:
        model = Url
        fields = ['id', 'url', 'snippet', 'user']
        read_only_fields = ('id',)


class SnippetUrlReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Url
        fields = ['id', 'url']
        read_only_fields = ('id',)