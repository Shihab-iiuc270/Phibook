from django.shortcuts import render
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action, api_view
from rest_framework.response import Response
from uuid import uuid4
from .models import Post, Like, Comment, PostImage
from .serializers import PostSerializer, CommentSerializer, EmptySerialiserz, PostImageSerializer
from .permissions import IsPosterOrReadonly, IsPostOwner
from .paginations import DefaultPagination
from drf_yasg.utils import swagger_auto_schema
# Create your views here.


class PostViewSet(viewsets.ModelViewSet):
    """"
    Api endpoint for managing post in Phibook 
    -Activation email to active a user with uid and token
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


@api_view(["POST"])
def initiate_payment(request):
    try:
        from sslcommerz_lib import SSLCOMMERZ
    except Exception as exc:
        return Response(
            {"error": "SSLCommerz library is not available", "details": str(exc)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    user = request.user
    amount = request.data.get('amount')
    if amount in (None, ""):
        return Response({"error": "amount is required"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        amount = float(amount)
        if amount <= 0:
            raise ValueError
    except (TypeError, ValueError):
        return Response({"error": "amount must be a positive number"}, status=status.HTTP_400_BAD_REQUEST)

    settings = {
        'store_id': "phibo69ab254643702",
        'store_pass': "phibo69ab254643702@ssl",
        'issandbox': True,
    }

    sslcz = SSLCOMMERZ(settings)
    post_body = {}
    post_body['total_amount'] = amount
    post_body['currency'] = "BDT"
    post_body['tran_id'] = uuid4().hex[:20]
    post_body['success_url'] = request.build_absolute_uri("/api/v1/payment/success/")
    post_body['fail_url'] = request.build_absolute_uri("/api/v1/payment/fail/")
    post_body['cancel_url'] = request.build_absolute_uri("/api/v1/payment/cancel/")
    post_body['emi_option'] = 0
    first_name = getattr(user, "first_name", "") or "Customer"
    last_name = getattr(user, "last_name", "") or ""
    email = getattr(user, "email", "") or request.data.get("email", "customer@example.com")
    phone = getattr(user, "phone_number", "") or request.data.get("phone", "01700000000")
    address = getattr(user, "location", "") or request.data.get("address", "Dhaka")

    post_body['cus_name'] = f"{first_name} {last_name}".strip()
    post_body['cus_email'] = email
    post_body['cus_phone'] = phone
    post_body['cus_add1'] = address
    post_body['cus_city'] = "Dhaka"
    post_body['cus_country'] = "Bangladesh"
    post_body['shipping_method'] = "NO"
    post_body['multi_card_name'] = ""
    post_body['num_of_item'] = 1
    post_body['product_name'] = "Test"
    post_body['product_category'] = "Test Category"
    post_body['product_profile'] = "general"


    try:
        response = sslcz.createSession(post_body)  # API response dict
    except Exception as exc:
        return Response(
            {"error": "payment gateway request failed", "details": str(exc)},
            status=status.HTTP_502_BAD_GATEWAY,
        )

    gateway_status = str(response.get("status", "")).upper() if isinstance(response, dict) else ""
    gateway_url = response.get("GatewayPageURL") if isinstance(response, dict) else None

    if gateway_status == "SUCCESS" and gateway_url:
        return Response({"payment_url": gateway_url}, status=status.HTTP_200_OK)

    return Response(
        {"error": "payment initiation failed", "gateway_response": response},
        status=status.HTTP_400_BAD_REQUEST,
    )


# Backward-compatible alias if any caller still imports the old name.
# initiate_Payment = initiate_payment
