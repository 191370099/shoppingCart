from rest_framework import serializers
from store.models import Cart, CartItem, Product


class ProductSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()

    class Meta:
        model = Product
        fields = '__all__'


class CartItemSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    product = ProductSerializer(read_only=True)
    price = serializers.SerializerMethodField()

    def get_price(self, cart_item: CartItem):
        return cart_item.product.price * cart_item.quantity

    class Meta:
        model = CartItem
        fields = ['id', 'quantity', 'product', 'price']


class CartSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    items = CartItemSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField()

    def get_total_price(self, cart: Cart):
        return sum([item.quantity * item.product.price for item in cart.items.all()])

    class Meta:
        model = Cart
        fields = ['id', 'is_active', 'items', 'total_price']


class AddCartItemSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField()

    def validate_product_id(self, value):
        if not Product.objects.filter(id=value).exists():
            raise serializers.ValidationError("Product does not exist")
        return value

    def save(self, **kwargs):
        cart_id = self.context['cart_pk']
        product_id = self.validated_data["product_id"]
        quantity = self.validated_data["quantity"]

        try:
            cart_item = CartItem.objects.get(cart_id=cart_id, product_id=product_id)
            cart_item.quantity += quantity
            cart_item.save()
            self.instance = cart_item
        except CartItem.DoesNotExist:
            self.instance = CartItem.objects.create(cart_id=cart_id, product_id=product_id, quantity=quantity)

        return self.instance

    class Meta:
        model = CartItem
        fields = ['id', 'product_id', 'quantity']


class UpdateCartItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = CartItem
        fields = ['quantity']
