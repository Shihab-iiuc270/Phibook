from djoser.serializers import  UserCreateSerializer as Base,UserSerializer as BaseUser
from rest_framework import exceptions, serializers

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

class UserSerializer(BaseUser):
    
    class Meta(BaseUser.Meta):
            fields = ['id','email','first_name','last_name','location','phone_number','avatar']
            ref_name = 'CustomUser'


