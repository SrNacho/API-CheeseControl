from rest_framework import serializers


class LecheSerializer(serializers.BaseSerializer):
    estado = serializers.CharField(max_length=100)
