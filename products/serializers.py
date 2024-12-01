from rest_framework import serializers
from .models import Brand, Category, Product, ProductImage, ProductReview, Supplier
from drf_spectacular.utils import extend_schema_field



class ProductWithCategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields =  ["name","slug"]


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ['name'] 

class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = ['name'] 

class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['image','img_alt','img_title']


class ProductSerializer(serializers.ModelSerializer):
    brand = BrandSerializer()
    supplier = SupplierSerializer()
    discount_percentage = serializers.SerializerMethodField()
    star_list = serializers.SerializerMethodField()
    images = serializers.SerializerMethodField() 
    category_breadcrumb = serializers.SerializerMethodField()
    category = ProductWithCategoriesSerializer()
    class Meta:
        model = Product
        fields = [
            'id', 'name', 'slug', 'images','category', 'selling_price', 'selling_old_price', 'purchase_price',
            'in_stock', 'brand', 'supplier','view_count', 'discount_percentage', 'star_list',
            'description', 'information','category_breadcrumb'
        ]
    
    def get_categories(self, obj):
        active_categories = obj.category.filter(is_active=True)
        return ProductWithCategoriesSerializer(active_categories, many=True).data

    @extend_schema_field(ProductImageSerializer(many=True))  # Swagger dökümantasyonu için açıklama ekliyoruz
    def get_images(self, obj):
        # İlişkili görselleri almak için doğru ilişkiyi kullanıyoruz
        images = obj.related_products.all()  # Görsellerin ilişkili olduğu model üzerinden alıyoruz
        return ProductImageSerializer(images, many=True).data  # Görselleri serileştirip döndürüyoruz
    
    # İndirim oranını hesaplamak
    @extend_schema_field(serializers.CharField) 
    def get_discount_percentage(self, obj):
        return obj.get_percentage()

    # Yıldız listesini almak
    @extend_schema_field(serializers.BooleanField) 
    def get_star_list(self, obj):
        return obj.get_star_list()
    
    @extend_schema_field(serializers.CharField) 
    def get_category_breadcrumb(self, obj):
        return obj.get_category_breadcrumb2()
    

