from djoser.serializers import  UserCreateSerializer as Base,UserSerializer as BaseUser
from rest_framework import exceptions, serializers

DEFAULT_AVATAR_PATH = "avatars/default-avatar-profile-icon-of-social-media-user-vector.jpg"

class UserCreateSerializer(Base):
    phone_number = serializers.CharField(
        write_only=True,
        required=False,
        allow_blank=True,
        allow_null=True,
    )
    location = serializers.CharField(
        write_only=True,
        required=False,
        allow_blank=True,
        allow_null=True,
    )
    avatar = serializers.ImageField(required=False, allow_null=True)
    class Meta(Base.Meta):
        fields = ['id','email','password','first_name','last_name','location','phone_number','avatar']

    def create(self, validated_data):
        # If client sends avatar as null/missing, force model default avatar.
        if validated_data.get("avatar") is None:
            validated_data.pop("avatar", None)
        return super().create(validated_data)


class UserSerializer(BaseUser):
    avatar = serializers.ImageField(required=False, allow_null=True)

    class Meta(BaseUser.Meta):
            fields = ['id','email','first_name','last_name','location','phone_number','avatar']
            ref_name = 'CustomUser'

    def update(self, instance, validated_data):
        # If client explicitly sends null, reset avatar to default.
        if "avatar" in validated_data and validated_data["avatar"] is None:
            validated_data["avatar"] = DEFAULT_AVATAR_PATH
        return super().update(instance, validated_data)


