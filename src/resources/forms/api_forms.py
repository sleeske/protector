from django.contrib.auth.hashers import check_password
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from resources.models import ProtectedResource


class ProtectedResourceCreateSerializer(serializers.Serializer):
    protected_url = serializers.CharField(required=False)
    protected_file = serializers.FileField(required=False)

    def validate(self, attrs):
        protected_url = attrs.get("protected_url")
        protected_file = attrs.get("protected_file")

        if not protected_url and not protected_file:
            raise ValidationError("Provice an URL or a file to protect.")

        if protected_url and protected_file:
            raise ValidationError(
                "Provice either an URL or a file to protect, not both."
            )

        return super().validate(attrs)


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

    def validate_password(self, value):
        if not check_password(value, self.instance.password):
            raise ValidationError("Invalid password")

        return value

    def get_resource_link(self, obj):
        request = self.context.get("request")
        return request.build_absolute_uri(obj.get_absolute_url())
