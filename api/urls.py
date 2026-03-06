from django.urls import path, include
from post.views import PostViewSet, CommentViewset, PostImageViewset, initiate_payment
from rest_framework_nested import routers
from users.views import UserSearchView
# from rest_framework.routers import DefaultRouter
# from rest_framework import routers

router = routers.DefaultRouter()
router.register('posts',PostViewSet, basename='post')
# router.register('categories', CategoryViewSet)
# router.register('carts', CartViewSet, basename='carts')
# router.register('orders', OrderViewset, basename='orders')

post_router = routers.NestedDefaultRouter(
    router, 'posts', lookup='post')
post_router.register('comments', CommentViewset, basename='post-comment')
post_router.register('images',PostImageViewset, basename='post-images')
# router.register('my_dashboard', views.DashboardViewSet, basename='my-dashboard')
# product_router.register('images', ProductImageViewSet,
#                         basename='product-images')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(post_router.urls)),
    path('users/search/', UserSearchView.as_view(), name='user-search'),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    path('payment/initiate/', initiate_payment, name='initiate-payment')
]
