from rest_framework import serializers
from .models import Post, Comment, Like,PostImage
from django.contrib.auth import get_user_model
# class CommentSerializer(serializers.ModelSerializer):
#     user = serializers.ReadOnlyField(source='user.username')
#     is_owner = serializers.SerializerMethodField()

#     class Meta:
#         model = Comment
#         fields = ['id', 'user', 'content', 'created_at', 'is_owner']

#     def get_is_owner(self, obj):
#         return obj.user == self.context['request'].user

class PostImageSerializer(serializers.ModelSerializer):
    image = serializers.ImageField()
    class Meta:
        model = PostImage
        fields =['id','image',]
class EmptySerialiserz(serializers.Serializer):
    pass
class SimpleUserSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField(
        method_name='get_current_user_name')

    class Meta:
        model = get_user_model()
        fields = ['id', 'name']

    def get_current_user_name(self, obj):
        return obj.get_full_name()


class CommentSerializer(serializers.ModelSerializer):
    # user = SimpleUserSerializer()
    user = serializers.SerializerMethodField(method_name='get_user')

    class Meta:
        model = Comment
        fields = ['id', 'user', 'content', 'updated_at']
        read_only_fields = ['user', 'post']

    def get_user(self, obj):
        return SimpleUserSerializer(obj.user).data

    def create(self, validated_data):
        post_id = self.context['post_id']
        return Comment.objects.create(post_id= post_id, **validated_data)
    
class PostSerializer(serializers.ModelSerializer):
    poster = SimpleUserSerializer(source = 'user',read_only = True)
    likes_count = serializers.IntegerField(source='likes.count', read_only=True,help_text = 'return the number of likes of the post')
    comments = CommentSerializer(many=True, read_only=True)
    is_liked = serializers.SerializerMethodField()
    caption = serializers.CharField(source = 'text')
    images = PostImageSerializer(many = True,read_only = True)
    class Meta:
        model = Post
        fields = ['id', 'poster', 'caption','images', 'likes_count', 'is_liked', 'comments', 'created_at','updated_at']

    def get_is_liked(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            return Like.objects.filter(post=obj, user=user).exists()
        return False
    