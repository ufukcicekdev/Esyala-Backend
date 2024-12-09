from rest_framework import serializers
from customerauth.models import Order, OrderItem
from customerauth.serializers import *
from drf_spectacular.utils import extend_schema_field

ORDER_STATUS_TRANSLATIONS = {
    'Pending': 'Beklemede',
    'Approved': 'Onaylandı',
    'Completed': 'Tamamlandı',
    'Cancelled': 'İptal Edildi',
}

class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['image', 'img_alt', 'img_title']

class OrderProductSerilazer(serializers.ModelSerializer):
    first_image = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['id', 'name', 'slug', 'first_image']

    @extend_schema_field(serializers.CharField)
    def get_first_image(self, obj):
        images = obj.related_products.all()
        if images.exists():
            return ProductImageSerializer(images.first()).data
        return None

class OrderItemListSerializer(serializers.ModelSerializer):
    product = OrderProductSerilazer()

    class Meta:
        model = OrderItem
        fields = ['product', 'quantity', 'rental_price', 'selling_price', 'is_rental', 'rental_period', 'subtotal', 'expired_date']

# Order'ı serileştirecek serializer
class OrderListSerializer(serializers.ModelSerializer):
    status_display = serializers.SerializerMethodField()
    class Meta:
        model = Order
        fields = [
            'order_number',  'total_amount','status_display',
             'created_at', 
            
        ]

    def get_status_display(self, obj):
        # Status'un Türkçe karşılığını döndürüyoruz
        return ORDER_STATUS_TRANSLATIONS.get(obj.status, obj.status)  
    


class OrderDetailSerializer(serializers.ModelSerializer):
    order_items = OrderItemListSerializer(many=True)
    order_city = CitySerializer()
    order_neighborhood = NeighborhoodSerializer()
    order_region = DistrictdSerializer()
    status_display = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = [
            'order_number', 'order_adress', 'billing_adress', 'total_amount', 'status_display',
            'billing_document', 'order_cancel_reason', 'order_cancel_date', 'created_at', 'updated_at', 
            'order_city', 'order_neighborhood', 'order_region', 'order_items'
        ]

    def get_status_display(self, obj):
        # Status'un Türkçe karşılığını döndürüyoruz
        return ORDER_STATUS_TRANSLATIONS.get(obj.status, obj.status) 