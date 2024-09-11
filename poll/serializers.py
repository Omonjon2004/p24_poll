from django.db.models import Model
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from account.models import Account
from poll.models import Choice, Poll, Vote


class PollSerializer(serializers.ModelSerializer):
    class Meta:
        model = Poll
        fields = ("id", "question", "published")


class PollPatchSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    question = serializers.CharField(required=False)
    author = serializers.PrimaryKeyRelatedField(
        queryset=Account.objects.all(), required=False
    )


class ChoiceSerializer(ModelSerializer):
    class Meta:
        model = Choice
        fields = ("id", "answer", "poll")


class VoteSerializer(ModelSerializer):
    class Meta:
        model = Vote
        fields = ("id", "choice", "voted_by", "voted_at")
        extra_kwargs = {
            "choice": {"read_only": True},
            "voted_at": {"read_only": True},
            "voted_by": {"read_only": True},
        }
