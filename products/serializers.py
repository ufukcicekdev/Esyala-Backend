from rest_framework import serializers
from .models import Answer, Brand, Cart, CartItem, Category, Product, ProductImage, ProductReview, Question, Supplier, ProductRentalPrice
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

class ProductRentalPriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductRentalPrice
        fields = ['name','rental_price','rental_old_price']


class ProductSerializer(serializers.ModelSerializer):
    brand = BrandSerializer()
    supplier = SupplierSerializer()
    discount_percentage = serializers.SerializerMethodField()
    star_list = serializers.SerializerMethodField()
    images = serializers.SerializerMethodField() 
    category_breadcrumb = serializers.SerializerMethodField()
    category = ProductWithCategoriesSerializer()
    rental_prices = serializers.SerializerMethodField()
    class Meta:
        model = Product
        fields = [
            'id', 'name', 'slug', 'images','category', 'selling_price', 'selling_old_price',
            'in_stock', 'brand', 'supplier','view_count', 'discount_percentage', 'star_list',
            'description', 'information','category_breadcrumb','rental_prices','view_count'
        ]
    
    def get_categories(self, obj):
        active_categories = obj.category.filter(is_active=True)
        return ProductWithCategoriesSerializer(active_categories, many=True).data

    @extend_schema_field(ProductImageSerializer(many=True))  
    def get_images(self, obj):
        images = obj.related_products.all()  
        return ProductImageSerializer(images, many=True).data  
    
    @extend_schema_field(serializers.CharField) 
    def get_discount_percentage(self, obj):
        return obj.get_percentage()

    @extend_schema_field(serializers.BooleanField) 
    def get_star_list(self, obj):
        return obj.get_star_list()
    
    @extend_schema_field(serializers.CharField) 
    def get_category_breadcrumb(self, obj):
        return obj.get_category_breadcrumb2()
    
    @extend_schema_field(ProductRentalPriceSerializer(many=True))  
    def get_rental_prices(self, obj):
        rental_prices = obj.related_products_price.all() 
        return ProductRentalPriceSerializer(rental_prices, many=True).data  
    


class ProductListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["slug"]



class ProductReviewSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.username', read_only=True)  
    class Meta:
        model = ProductReview
        fields = ['id', 'user', 'user_name', 'product', 'rating', 'comment', 'created_at']



class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ['id', 'answer_text', 'created_at']

class QuestionSerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(many=True, read_only=True) 

    class Meta:
        model = Question
        fields = ['id', 'question_text', 'created_at', 'is_answered', 'answers']


class QuestionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['user', 'question_text', 'product']



class ProductCartItemSerializer(serializers.ModelSerializer):

    category = ProductWithCategoriesSerializer()
    first_image =  serializers.SerializerMethodField() 
    discount_percentage = serializers.SerializerMethodField()
    rental_prices = serializers.SerializerMethodField()
    class Meta:
        model = Product
        fields = ['id', 'name', 'slug', 'first_image', 'selling_price','selling_old_price','purchase_price',
                'in_stock', 'category', 'discount_percentage','rental_prices'] 
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
    
    @extend_schema_field(ProductRentalPriceSerializer(many=True))  
    def get_rental_prices(self, obj):
        rental_prices = obj.related_products_price.all() 
        return ProductRentalPriceSerializer(rental_prices, many=True).data  

    
    

class CartItemSerializer(serializers.ModelSerializer):
    product = ProductCartItemSerializer()

    class Meta:
        model = CartItem
        fields = ['id', 'product', 'quantity', 'is_rental', 'rental_price', 'rental_period', 'selling_price','cart_id']


class CartSerializer(serializers.ModelSerializer):
    cart_items = serializers.SerializerMethodField()
    total_price = serializers.SerializerMethodField()  # Toplam fiyat alanı

    class Meta:
        model = Cart
        fields = ['id', 'user', 'session_key', 'cart_items', 'created_at', 'updated_at', 'order_completed', 'total_price']

    def get_cart_items(self, obj):
        cart_items = obj.get_cart_items()
        return CartItemSerializer(cart_items, many=True).data

    def get_total_price(self, obj):
        # Sepet içerisindeki tüm ürünlerin toplam fiyatını hesaplamak
        total_price = 0
        cart_items = obj.get_cart_items()  # Sepet ürünlerini al

        for item in cart_items:
            if item.is_rental:
                # Kiralık ürünler için kira fiyatını kullan
                total_price += float(item.rental_price) * float(item.quantity)
            else:
                # Satılık ürünler için satış fiyatını kullan
                total_price += float(item.selling_price) * float(item.quantity)

        return total_price





