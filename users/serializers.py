from djoser.serializers import  UserCreateSerializer as Base,UserSerializer as BaseUser
from rest_framework import exceptions, serializers

class UserCreateSerializer(Base):
    phone_number = serializers.CharField(write_only=True)
    location = serializers.CharField(write_only=True)
    class Meta(Base.Meta):
        fields = ['id','email','password','first_name','last_name','location','phone_number']

class UserSerializer(BaseUser):
    
    class Meta(BaseUser.Meta):
            fields = ['id','email','first_name','last_name','location','phone_number']
            ref_name = 'CustomUser'


