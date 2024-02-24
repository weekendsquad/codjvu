from rest_framework import serializers
from .models import Setting


class SettingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Setting
        fields = ['key', 'value']
        read_only_fields = ('id',)
