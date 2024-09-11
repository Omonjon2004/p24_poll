from trace import Trace

from django.shortcuts import get_object_or_404, render
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.authentication import (BasicAuthentication,
                                           TokenAuthentication)
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from poll.models import Choice, Poll, Vote
from poll.serializers import (ChoiceSerializer, PollPatchSerializer,
                              PollSerializer, VoteSerializer)

"""
CRUD
Create
Read
Update- >   PUT -> obyekt yaratish uchun kerak boladigan hamma fiedlar berilishi kerak.
            PATCH -> ozgartirilishi kerak bolgan fieldlar berilsa boldi.
Delete
"""


# class PollsView(APIView):
#     permission_classes = [IsAuthenticated, ]
#     authentication_classes = (BasicAuthentication, TokenAuthentication)
#
#     def get(self, request):
#         polls = Poll.objects.filter(author=request.user)
#         serializer = PollSerializer(polls, many=True)
#         return Response(data=serializer.data, status=status.HTTP_200_OK)
#
#     @swagger_auto_schema(
#         request_body=PollSerializer,
#         operation_description="This endpoint for creating Poll Object"
#     )
#     def post(self, request):
#         serializer = PollSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save(author=request.user)
#             return Response(data=serializer.data, status=status.HTTP_201_CREATED)
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#
# class PollView(APIView):
#     def get(self, request, pk):
#         poll = get_object_or_404(Poll, pk=pk)
#         serializer = PollSerializer(poll)
#         return Response(data=serializer.data, status=status.HTTP_200_OK)
#
#     def put(self, request, pk):
#         poll = get_object_or_404(Poll, pk=pk)
#         serializer = PollSerializer(data=request.data, instance=poll)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(data={"message": "Object successfully updated"}, status=status.HTTP_202_ACCEPTED)
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     def patch(self, request, pk):
#         poll = get_object_or_404(Poll, pk=pk)
#         serializer = PollPatchSerializer(data=request.data, instance=poll)
#         if serializer.is_valid():
#             data = serializer.validated_data
#             for key, value in data.items():
#                 setattr(poll, key, value)
#             poll.save()
#             return Response(data=serializer.data, status=status.HTTP_202_ACCEPTED)
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     def delete(self, request, pk):
#         poll = get_object_or_404(Poll, pk=pk)
#         poll.delete()
#         return Response(data={"message": "Object successfully deleted"}, status=status.HTTP_202_ACCEPTED)
#
class PollViewSet(ModelViewSet):
    queryset = Poll.objects.all()
    serializer_class = PollSerializer
    my_tags = ("poll",)
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
        super().perform_create(serializer)


class ChoiceViewSet(ModelViewSet):
    queryset = Choice.objects.all()
    serializer_class = ChoiceSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)
    my_tags = ("choice",)

    @action(detail=True, methods=["post"])
    def vote(self, *args, **kwargs):
        choice = self.get_object()
        user = self.request.user
        vote = Vote.objects.create(choice=choice, poll=choice.poll, voted_by=user)
        serializer = VoteSerializer(vote)
        return Response(data=serializer.data)

    def perform_create(self, serializer):
        super().perform_create(serializer)
