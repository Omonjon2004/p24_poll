from trace import Trace

from django.db.models import Count
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ViewSet
from yaml import serialize

from account.models import Account, Interest
from account.serializers import (AccountDetailSerializer, AccountSerializer,
                                 InterestSerializer)


class AccountView(ModelViewSet):
    serializer_class = AccountSerializer
    queryset = Account.objects.all()
    serializer_class2 = AccountDetailSerializer
    my_tags = ("account",)

    @action(
        methods=["get"],
        detail=True,
    )
    def interests(self, *args, **kwargs):
        account = self.get_object()
        serializer = InterestSerializer(account.profile.interests.all(), many=True)
        return Response(data=serializer.data)

    # api/v1/account/top-contacts/
    @action(methods=["POST"], detail=False, url_path="top-accounts")
    def top_accounts(self, *args, **kwargs):
        queryset = self.get_queryset()
        # queryset = queryset.filter(profile__interests__isnull=False).distinct()
        queryset = (
            queryset.annotate(interest_count=Count("profile__interests"))
            .filter(interest_count__gt=0)
            .order_by("-interest_count")
        )
        serializer = self.serializer_class(queryset, many=True)
        return Response(data=serializer.data)

    # # create list -> AccountSerializer
    # # detail, put, patch, delete -> AccountDetailSerializer
    def retrieve(self, request, pk=None):
        account = get_object_or_404(self.queryset, pk=pk)
        serializer = self.serializer_class2(account)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, pk=None):
        account = get_object_or_404(self.queryset, pk=pk)
        serializer = self.serializer_class2(data=request.data, instance=account)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

    def partial_update(self, request, pk=None):
        account = get_object_or_404(self.queryset, pk=pk)
        serializer = self.serializer_class2(
            data=request.data, instance=account, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)


class InterestView(ViewSet):
    queryset = Interest.objects.all()
    serializer_class = InterestSerializer
    my_tags = ("interest",)

    def list(self, request):
        serializer = InterestSerializer(self.queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def partial_update(self, request, pk):
        interest = get_object_or_404(Interest, pk=pk)
        serializer = self.serializer_class(
            instance=interest, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data=serializer.data)
