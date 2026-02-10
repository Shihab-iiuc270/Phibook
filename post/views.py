from django.shortcuts import render
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Post, Like, Comment,PostImage
from .serializers import PostSerializer, CommentSerializer,EmptySerialiserz,PostImageSerializer
from .permissions import IsPosterOrReadonly,IsPostOwner
from .paginations import DefaultPagination
from drf_yasg.utils import swagger_auto_schema
# Create your views here.


class PostViewSet(viewsets.ModelViewSet):
    """"
    Api endpoint for managing post in Phibook 
    - Anyone can See Posts
    - Only the Authenticated user can Post
    - Only the poster can edit their post
    """
    queryset = Post.objects.all().order_by('-created_at')
    serializer_class = PostSerializer
    pagination_class = DefaultPagination
    def get_permissions(self):
        if self.action == 'toggle_like':
            permission_classes = [permissions.IsAuthenticated]
        else:
            permission_classes = [IsPosterOrReadonly]
        return [permission() for permission in permission_classes]
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['post'],serializer_class=EmptySerialiserz)
    def toggle_like(self, request, pk=None):
        post = self.get_object()
        like_queryset = Like.objects.filter(user=request.user, post=post)
        
        if like_queryset.exists():
            like_queryset.delete()
            return Response({'status': 'unliked', 'likes_count': post.likes.count()})
        else:
            Like.objects.create(user=request.user, post=post)
            return Response({'status': 'liked', 'likes_count': post.likes.count()})

    @action(detail=False, methods=['GET', 'POST'], serializer_class=PostSerializer)
    def my_dashboard(self, request):
        if request.method == 'GET':
            my_posts = Post.objects.filter(user=request.user).prefetch_related('comments')
            serializer = self.get_serializer(my_posts, many=True)
            return Response(serializer.data)
        
        elif request.method == 'POST':
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid():
                serializer.save(user=request.user)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    @swagger_auto_schema(
            operation_summary= 'Retreive a list of post'
    )
    def list(self, request, *args, **kwargs):
        """Retreive all the Post"""
        return super().list(request, *args, **kwargs)
    @swagger_auto_schema(
            operation_summary= 'Create a post by Logged in User',
            request_body= PostSerializer,
            responses={
                201 : PostSerializer,
                400 : "Bad Request"
            }
    )
    def create(self, request, *args, **kwargs):
        """Only the Authenticated user can Post"""
        return super().create(request, *args, **kwargs)

class PostImageViewset(viewsets.ModelViewSet):
    serializer_class = PostImageSerializer
    permission_classes = [IsPostOwner,permissions.IsAuthenticated]

    def get_queryset(self):
        return PostImage.objects.filter(post_id= self.kwargs.get('post_pk'))
    def perform_create(self, serializer):
        serializer.save(post_id= self.kwargs.get('post_pk'))
    

class CommentViewset(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsPosterOrReadonly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        return Comment.objects.filter(post_id=self.kwargs.get('post_pk'))

    def get_serializer_context(self):
        return {'post_id': self.kwargs.get('post_pk')}