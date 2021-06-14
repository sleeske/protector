from rest_framework import serializers

from resources.models import ProtectedResource


class ProtectedResourceCreateSerializer(serializers.Serializer):
    protected_url = serializers.CharField(required=False)
    protected_file = serializers.FileField(required=False)


class ProtectedResourceAuthorizationSerializer(serializers.ModelSerializer):
    resource_type_display = serializers.CharField(
        source="get_resource_type_display", read_only=True
    )
    resource_link = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = ProtectedResource
        fields = (
            "password",
            "resource_type",
            "resource_type_display",
            "resource_link",
        )
        read_only_fields = (
            "resource_type",
            "resource_type_display",
            "resource_link",
        )
        extra_kwargs = {"password": {"write_only": True}}

    def get_resource_link(self, obj):
        request = self.context.get("request")
        return request.build_absolute_uri(obj.get_absolute_url())
