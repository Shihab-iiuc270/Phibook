from django.urls import path,include
from rest_framework_nested import routers
# from rest_framework.routers import DefaultRouter
from post import views
# from rest_framework import routers

router = routers.DefaultRouter()
router.register('posts', views.PostViewSet, basename='post')
# router.register('categories', CategoryViewSet)
# router.register('carts', CartViewSet, basename='carts')
# router.register('orders', OrderViewset, basename='orders')

post_router = routers.NestedDefaultRouter(
    router, 'posts', lookup='post')
post_router.register('comments', views.CommentViewset, basename='post-comment')
# router.register('my_dashboard', views.DashboardViewSet, basename='my-dashboard')
# product_router.register('images', ProductImageViewSet,
#                         basename='product-images')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(post_router.urls)),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
]
