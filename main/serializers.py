from rest_framework import serializers
from .models  import *
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from products.models import Product, Brand, Supplier, Category, ProductImage, RoomType, HomeType, HomeModel, SpaceDefinition, TimeRange
import re
from drf_spectacular.utils import extend_schema_field
from bs4 import BeautifulSoup

class HomeMainBannerSerializer(serializers.ModelSerializer):
    class Meta():
        model = HomeMainBanner
        fields = "__all__"


class HomeSubBannerSerializer(serializers.ModelSerializer):
    class Meta():
        model = HomeSubBanner
        fields = "__all__"


class SocialMediaSerializer(serializers.ModelSerializer):
    class Meta():
        model = SocialMedia
        fields = ["name","link"]


class AboutPageSerializer(serializers.ModelSerializer):
    social_media_links = serializers.SerializerMethodField()
    class Meta():
        model = TeamMembers
        fields = ["full_name", "image", "position", "social_media_links", "level"]
    
    @extend_schema_field(serializers.CharField) 
    def get_social_media_links(self, obj):
        return obj.get_social_media_links()



class ContactUsSerializer(serializers.ModelSerializer):
    class Meta():
        model = ContactUs
        fields = ["full_name", "email", "phone", "subject", "message"]

    def validate_email(self, value):
        try:
            validate_email(value)
        except ValidationError:
            raise serializers.ValidationError("Lütfen geçerli bir e-posta adresi girin.")
        return value
    
    def validate_phone(self, value):
        if not re.match(r'^\+?[0-9]\d{1,10}$', value):
            raise serializers.ValidationError("Lütfen geçerli bir telefon numarası girin.")
        return value

    def validate_message(self, value):
        if len(value) < 10:
            raise serializers.ValidationError("Mesaj en az 10 karakter olmalıdır.")
        return value


class ProductWithCategoriesSerializer(serializers.ModelSerializer):
    product_count = serializers.SerializerMethodField()
    class Meta:
        model = Category
        fields =  ["name","slug","product_count"]

    @extend_schema_field(serializers.IntegerField) 
    def product_count(self, obj):
        return obj.product_count() 


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
    category = ProductWithCategoriesSerializer()
    images = ProductImageSerializer(source='related_products', many=True, read_only=True)
    class Meta:
        model = Product
        fields = "__all__"


    def get_categories(self, obj):
        active_categories = obj.category.filter(is_active=True)
        return ProductWithCategoriesSerializer(active_categories, many=True).data



class GetCategorySerializer(serializers.ModelSerializer):
    children = serializers.SerializerMethodField()
    class Meta:
        model = Category
        fields = ["name", "slug", "children"]


    def get_children(self, obj):
        if obj.children.exists():
            return GetCategorySerializer(obj.children.filter(is_active=True), many=True).data
        return []
    

class GetFooterCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["name", "slug"]


class GetBrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = "__all__"


class RoomTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomType
        fields = "__all__"

class HomeTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = HomeType
        fields = "__all__"

class HomeModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = HomeModel
        fields = "__all__"

class SpaceDefSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpaceDefinition
        fields = "__all__"

class TimeRangeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimeRange
        fields = "__all__"

class CategoryProductSerializers(serializers.ModelSerializer):
    brand = BrandSerializer()  
    supplier = SupplierSerializer()
    category = ProductWithCategoriesSerializer()
    first_image =  serializers.SerializerMethodField() 
    discount_percentage = serializers.SerializerMethodField()
    truncated_description = serializers.SerializerMethodField()
    star_list = serializers.SerializerMethodField()
    room_types = RoomTypeSerializer(many=True, read_only=True)
    home_types = HomeTypeSerializer(many=True, read_only=True)
    home_models = HomeModelSerializer(many=True, read_only=True)
    space_definitions = SpaceDefSerializer(many=True, read_only=True)
    time_ranges = TimeRangeSerializer(many=True, read_only=True)
    class Meta:
        model = Product
        fields = ['id', 'name', 'slug', 'first_image', 'selling_price','selling_old_price','purchase_price',
                'in_stock', 'brand', 'supplier', 'category','view_count', 'discount_percentage','star_list', 
                'room_types','home_types','home_models', 'space_definitions','time_ranges','truncated_description'] 
    def get_categories(self, obj):
        active_categories = obj.category.filter(is_active=True)
        return ProductWithCategoriesSerializer(active_categories, many=True).data
    
    @extend_schema_field(serializers.CharField) 
    def get_first_image(self, obj):
        images = obj.related_products.all() 
        if images.exists():
            return ProductImageSerializer(images.first()).data  
        return None 
    @extend_schema_field(serializers.CharField) 
    def get_discount_percentage(self, obj):
        return obj.get_percentage() 
    @extend_schema_field(serializers.BooleanField) 
    def get_star_list(self, obj):
        return obj.get_star_list() 
    
    @extend_schema_field(serializers.CharField) 
    def get_truncated_description(self, obj):
        return obj.truncated_description() 




class SubscriptionSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    class Meta:
        model = Subscription
        fields = ['email']