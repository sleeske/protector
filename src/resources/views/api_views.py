from django.utils.crypto import get_random_string
from rest_framework import status
from rest_framework.generics import CreateAPIView, GenericAPIView, RetrieveAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from resources.forms.api_forms import (
    ProtectedResourceAuthorizationSerializer,
    ProtectedResourceCreateSerializer,
)
from resources.models import ProtectedResource
from resources.services import (
    create_protected_resource_with_username_and_password,
    increment_visitors_count,
    is_resource_expired,
)
from resources.utils.crypto import password_factory


class ProtectedResourceCreateAPIView(CreateAPIView):
    serializer_class = ProtectedResourceCreateSerializer
    password_factory = get_random_string
    permission_classes = (IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        obj = create_protected_resource_with_username_and_password(
            self.request.user, password_factory(), **serializer.validated_data
        )

        return Response(
            data={
                "password": obj._password,
                "authorization_url": self.request.build_absolute_uri(
                    obj.get_api_authorization_url()
                ),
            },
            status=status.HTTP_201_CREATED,
        )


class ProtectedResourceAuthorizationAPIView(GenericAPIView):
    serializer_class = ProtectedResourceAuthorizationSerializer
    permission_classes = (AllowAny,)
    queryset = ProtectedResource.objects.all()
    lookup_field = "access_id"

    def post(self, request, *args, **kwargs):
        instance = self.get_object()
        if is_resource_expired(instance):
            return Response("Resource link expired.", status=status.HTTP_410_GONE)

        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        increment_visitors_count(instance)

        return Response(serializer.data)


class ProtectedResourceStats(RetrieveAPIView):
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return ProtectedResource.objects.created_by(
            self.request.user
        ).count_visited_links_and_files()

    def retrieve(self, request, *args, **kwargs):
        return Response(
            data={item.pop("date_created"): item for item in self.get_queryset()}
        )
