from rest_framework import permissions
from .models import Post

class IsPosterOrReadonly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        if request.user.is_staff:
            return True

        return obj.user == request.user
    
class IsPostOwner(permissions.BasePermission):
    """Custom permission to only allow owners of a post to add images."""
    
    def has_permission(self, request, view):
        # For create/update/delete actions
        if request.method in ['POST', 'PUT', 'PATCH', 'DELETE']:
            # Get post_id from URL kwargs
            post_id = view.kwargs.get('post_pk')
            if not post_id:
                return False
            
            try:
                post = Post.objects.get(id=post_id)
                return post.user == request.user
            except Post.DoesNotExist:
                return False
        # Allow GET requests (list, retrieve)
        return True