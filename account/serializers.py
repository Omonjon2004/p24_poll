from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from account.models import Account, AccountProfile, Interest


class AccountSerializer(ModelSerializer):
    password = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    def validate(self, attrs):
        if attrs.get("password") != attrs.get("password2"):
            raise serializers.ValidationError("Passwords must be match")
        return attrs

    def create(self, validated_data):
        validated_data.pop("password2")
        account: Account = super().create(validated_data)
        account.set_password(validated_data["password"])
        account.save()
        return account

    class Meta:
        model = Account
        fields = (
            "id",
            "first_name",
            "last_name",
            "username",
            "email",
            "password",
            "password2",
            "phone",
        )
        extra_kwargs = {
            "email": {"required": True, "allow_null": False},
            "first_name": {"required": True, "allow_null": False},
            "last_name": {"required": True, "allow_null": False},
        }


class InterestSerializer(ModelSerializer):
    class Meta:
        model = Interest
        fields = (
            "id",
            "name",
        )


class AccountProfileSerializer(ModelSerializer):
    passport_number = serializers.CharField(required=False)
    passport_letter = serializers.CharField(required=False)

    class Meta:
        model = AccountProfile
        fields = ("city", "passport_number", "passport_letter", "interests")
        extra_kwargs = {
            "interests": {"required": False, "allow_null": True, "allow_empty": True},
        }

    def to_representation(self, instance: AccountProfile):
        representation = super().to_representation(instance)
        representation["interests"] = InterestSerializer(
            instance.interests.all(), many=True
        ).data
        return representation


class AccountDetailSerializer(ModelSerializer):
    profile = AccountProfileSerializer(allow_null=True, required=False)

    class Meta:
        model = Account
        fields = (
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "phone",
            "profile",
        )
        extra_kwargs = {
            "email": {"required": False, "allow_null": True},
            "first_name": {"required": False, "allow_null": True},
            "last_name": {"required": False, "allow_null": True},
            "profile": {"required": False, "allow_null": True},
        }



    def update(self, instance, validated_data):
        profile = validated_data.pop("profile")
        super().update(instance, validated_data)
        account_profile: AccountProfile = instance.profile
        if profile:
            intrests = profile.pop("interests", None)
            for key, value in profile.items():
                setattr(account_profile, key, value)
            if intrests or isinstance(intrests, list):
                account_profile.interests.set(intrests)
            account_profile.save()
        return instance
