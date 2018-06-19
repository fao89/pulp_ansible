from django.db import transaction
from django_filters.rest_framework import filterset
from rest_framework.decorators import detail_route
from rest_framework import status
from rest_framework.response import Response

from pulpcore.plugin.models import Artifact, RepositoryVersion
from pulpcore.plugin.serializers import (
    RepositoryPublishURLSerializer,
    RepositorySyncURLSerializer,
)
from pulpcore.plugin.tasking import enqueue_with_reservation
from pulpcore.plugin.viewsets import (
    ContentViewSet,
    RemoteViewSet,
    OperationPostponedResponse,
    PublisherViewSet
)

from . import tasks
from .models import AnsibleRemote, AnsiblePublisher, AnsibleRole, AnsibleRoleVersion
from .serializers import (AnsibleRemoteSerializer, AnsiblePublisherSerializer,
                          AnsibleRoleSerializer, AnsibleRoleVersionSerializer)


class AnsibleRoleFilter(filterset.FilterSet):
    class Meta:
        model = AnsibleRole
        fields = [
            'name',
            'namespace'
        ]


class AnsibleRoleVersionFilter(filterset.FilterSet):
    class Meta:
        model = AnsibleRoleVersion
        fields = [
            'version',
        ]


class AnsibleRoleViewSet(ContentViewSet):
    endpoint_name = 'ansible/roles'
    router_lookup = 'role'
    queryset = AnsibleRole.objects.all()
    serializer_class = AnsibleRoleSerializer
    filter_class = AnsibleRoleFilter

    @transaction.atomic
    def create(self, request):
        # TODO: we should probably remove create() from ContentViewSet
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class AnsibleRoleVersionViewSet(ContentViewSet):
    endpoint_name = 'versions'
    nest_prefix = 'ansible/roles'
    router_lookup = 'roleversion'
    parent_viewset = AnsibleRoleViewSet
    parent_lookup_kwargs = {'role_pk': 'role__pk'}
    queryset = AnsibleRoleVersion.objects.all()
    serializer_class = AnsibleRoleVersionSerializer
    filter_class = AnsibleRoleVersionFilter

    @classmethod
    def endpoint_pieces(cls):
        return (cls.endpoint_name,)

    @transaction.atomic
    def create(self, request, role_pk):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data

        role_version = AnsibleRoleVersion(**validated_data)
        role_version.role = AnsibleRole.objects.get(pk=role_pk)
        role_version.save()
        role_version.artifact = self.get_resource(request.data['artifact'], Artifact)

        headers = self.get_success_headers(request.data)
        return Response(self.get_serializer(role_version).data, status=status.HTTP_201_CREATED,
                        headers=headers)


class AnsibleRemoteViewSet(RemoteViewSet):
    endpoint_name = 'ansible'
    queryset = AnsibleRemote.objects.all()
    serializer_class = AnsibleRemoteSerializer

    @detail_route(methods=('post',), serializer_class=RepositorySyncURLSerializer)
    def sync(self, request, pk):
        remote = self.get_object()
        serializer = RepositorySyncURLSerializer(
            data=request.data,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        repository = serializer.validated_data.get('repository')
        result = enqueue_with_reservation(
            tasks.synchronize,
            [repository, remote],
            kwargs={
                'remote_pk': remote.pk,
                'repository_pk': repository.pk
            }
        )
        return OperationPostponedResponse(result, request)


class AnsiblePublisherViewSet(PublisherViewSet):
    endpoint_name = 'ansible'
    queryset = AnsiblePublisher.objects.all()
    serializer_class = AnsiblePublisherSerializer

    @detail_route(methods=('post',), serializer_class=RepositoryPublishURLSerializer)
    def publish(self, request, pk):
        publisher = self.get_object()
        serializer = RepositoryPublishURLSerializer(
            data=request.data,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        repository_version = serializer.validated_data.get('repository_version')

        # Safe because version OR repository is enforced by serializer.
        if not repository_version:
            repository = serializer.validated_data.get('repository')
            repository_version = RepositoryVersion.latest(repository)
        result = enqueue_with_reservation(
            tasks.publish, [repository_version.repository, publisher],
            kwargs={
                'publisher_pk': str(publisher.pk),
                'repository_version_pk': str(repository_version.pk)
            }
        )
        return OperationPostponedResponse(result, request)