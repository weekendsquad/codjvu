from rest_framework import serializers
from snippet.models import Language
from .models import Setting


class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language
        fields = ['id', 'language']
        read_only_fields = ('id',)


class SettingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Setting
        fields = ['key', 'value']
        read_only_fields = ('id',)
