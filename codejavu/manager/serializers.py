from rest_framework import serializers
from snippet.models import Language


class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language
        fields = ['id', 'language']
        read_only_fields = ('id',)
