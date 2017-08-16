from django.db.models import Q

from rest_framework import generics, permissions, status
from rest_framework.compat import is_anonymous
from rest_framework.exceptions import APIException
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from group.serializer.group import GroupSerializer, MainGroupListSerializer, GroupDetailSerializer
from group.pagination import GroupPagination
from utils.permissions import AuthorIsRequestUser
from ..models import Group

__all__ = (
    'MainGroupListView',
    'AllGroupListView',
    'GroupRegisterView',
    'GroupRetrieveView',
    'GroupUpdateView',
    'GroupDestroyView',
    'GroupLikeToggleView',
    'GroupJoinView',
)


class MainGroupListView(APIView):
    def get(self, request, *args, **kwargs):
        if not is_anonymous(self.request.user):
            origin_lat = float(self.request.GET.get('lat', self.request.user.lat))
            origin_lng = float(self.request.GET.get('lng', self.request.user.lng))
            distance_limit = float(self.request.GET.get('distance_limit', 0.5))
            hobby = self.request.GET.get('hobby', self.request.user.hobby).split(',')

            groups = Group.objects.iterator()
            filter_group_pk_list = []
            for group in groups:
                distance = group.get_distance(origin_lat, origin_lng)
                if distance < distance_limit:
                    filter_group_pk_list.append(group.pk)
            if not len(filter_group_pk_list):
                raise APIException({'result': '검색결과가 없습니다.'})

            if len(hobby) == 1:
                queryset = Group.objects.filter(pk__in=filter_group_pk_list).filter(hobby__in=hobby)
            else:
                queryset = Group.objects.filter(pk__in=filter_group_pk_list).filter(hobby__in=hobby)

            if not queryset:
                raise APIException({'result': '검색결과가 없습니다.'})

            serializer = MainGroupListSerializer(queryset, many=True)

            return Response(serializer.data)
        origin_lat = float(self.request.GET.get('lat', 37.517547))
        origin_lng = float(self.request.GET.get('lng', 127.018127))
        distance_limit = float(self.request.GET.get('distance_limit', 0.5))
        if self.request.GET.get('hobby') is None:
            hobby = None
        else:
            hobby = self.request.GET.get('hobby').split(',')

        groups = Group.objects.iterator()
        filter_group_pk_list = []
        for group in groups:
            distance = group.get_distance(origin_lat, origin_lng)
            if distance < distance_limit:
                filter_group_pk_list.append(group.pk)
        if not len(filter_group_pk_list):
            raise APIException({'result': '검색결과가 없습니다.'})

        if not hobby:
            queryset = Group.objects.filter(pk__in=filter_group_pk_list)
        elif len(hobby) == 1:
            queryset = Group.objects.filter(pk__in=filter_group_pk_list).filter(hobby__in=hobby)
        else:
            queryset = Group.objects.filter(pk__in=filter_group_pk_list).filter(hobby__in=hobby)

        serializer = MainGroupListSerializer(queryset, many=True)

        return Response(serializer.data)


class AllGroupListView(generics.ListAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupDetailSerializer
    pagination_class = GroupPagination


class GroupRegisterView(generics.CreateAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = (
        permissions.IsAuthenticated,
    )

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response({"pk": serializer.data['pk']}, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class GroupRetrieveView(generics.RetrieveAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupDetailSerializer
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
    )


class GroupUpdateView(APIView):
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        AuthorIsRequestUser
    )

    def put(self, request, group_pk, **kwargs):
        partial = kwargs.pop('partial', True)
        instance = Group.objects.get(pk=group_pk)
        serializer = GroupSerializer(instance, data=request.data, partial=partial)
        if request.user == instance.author:
            serializer.is_valid(raise_exception=True)
            serializer.save()
        else:
            raise APIException({"detail": "권한이 없습니다."})
        ret = {
            "pk": serializer.data['pk']
        }
        return Response(ret)


class GroupDestroyView(APIView):
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
    )

    def delete(self, request, group_pk):
        instance = Group.objects.get(pk=group_pk)

        if request.user == instance.author:
            instance.delete()
        else:
            raise APIException({"detail": "권한이 없습니다."})
        ret = {
            "detail": "모임이 삭제되었습니다."
        }
        return Response(ret)


class GroupLikeToggleView(APIView):
    def post(self, request, group_pk):
        instance = get_object_or_404(Group, pk=group_pk)
        group_like, group_like_created = instance.grouplike_set.get_or_create(
            user=request.user
        )
        if not group_like_created:
            group_like.delete()
        return Response({'created': group_like_created})


class GroupJoinView(APIView):
    permission_classes = (
        permissions.IsAuthenticated,
    )

    def post(self, request, group_pk):
        instance = get_object_or_404(Group, pk=group_pk)
        if instance.members.filter(pk=request.user.pk):
            raise APIException({'joined': '이미 가입한 모임입니다.'})
        instance.members.add(request.user)
        return Response({'joined': True})
