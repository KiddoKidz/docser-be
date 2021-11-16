import sys

from rest_framework import serializers


class FileSearchSerializer(serializers.Serializer):
    q = serializers.CharField(allow_blank=True, required=False, default="")
    mime_types = serializers.ListField(
        child=serializers.CharField(), allow_empty=True, required=False, default=[]
    )
    start_time = serializers.IntegerField(required=False, default=0)
    end_time = serializers.IntegerField(required=False, default=sys.maxsize)
    owners = serializers.ListField(
        child=serializers.CharField(), allow_empty=True, required=False, default=[]
    )
    shared_by = serializers.ListField(
        child=serializers.CharField(), allow_empty=True, required=False, default=[]
    )
    locations = serializers.ListField(
        child=serializers.CharField(), allow_empty=True, required=False, default=[]
    )

    def validate_start_time(self, value):
        if value < 0:
            raise serializers.ValidationError("start_time must be positive value")
        return value

    def validate_end_time(self, value):
        if value < 0:
            raise serializers.ValidationError("end_time must be positive value")
        return value


class FileLocationSearchSerializer(serializers.Serializer):
    q = serializers.CharField(allow_blank=True, required=False, default="")


class FileOwnerSearchSerializer(serializers.Serializer):
    q = serializers.CharField(allow_blank=True, required=False, default="")
