from django.urls import path, include
from rest_framework_nested import routers

from store.views import CartViewSet, ProductViewSet, CartItemViewSet

router = routers.DefaultRouter()
router.register('carts', CartViewSet)
router.register('products', ProductViewSet)
item_router = routers.NestedDefaultRouter(router, r'carts', lookup='cart')
item_router.register('items', CartItemViewSet, basename='cart-items')
urlpatterns = router.urls + item_router.urls
