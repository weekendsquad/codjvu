from rest_framework import serializers
from rest_framework.fields import empty

from snippet.models import Tag, Snippet, SnippetTag, Url, Language


class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language
        fields = ['id', 'language']
        read_only_fields = ('id',)


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
        fields = ['id', 'user', 'snippet', 'title', 'language']
        read_only_fields = ('id',)


class SnippetReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Snippet
        fields = ['id', 'title', 'language']
        read_only_fields = ('id',)


class SnippetTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = SnippetTag
        fields = ['id', 'tag', 'snippet']
        read_only_fields = ('id',)


class SnippetTagReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = SnippetTag
        fields = ['tag']


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
