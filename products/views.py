from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Cart, CartItem, Product, ProductReview, Question
from .serializers import CartItemSerializer, CartSerializer, ProductReviewSerializer, ProductSerializer, ProductListSerializer, QuestionCreateSerializer, QuestionSerializer
from customerauth.models import UserProductView
from django.shortcuts import get_object_or_404
from django.db.models import Avg
from rest_framework import status
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated, AllowAny
from django.db.models import F

class ProductDetailView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, product_slug):
        product = get_object_or_404(Product, slug=product_slug, is_active=True)
        
        Product.objects.filter(pk=product.pk).update(view_count=F('view_count') + 1)

        reviews = ProductReview.objects.filter(product=product)
        average_rating = int(reviews.aggregate(Avg('rating'))['rating__avg'] or 0)

        if request.user.is_authenticated:
            user_product_view, created = UserProductView.objects.get_or_create(user=request.user, product=product)
            if not created:
                user_product_view.created_date = timezone.now()  
                user_product_view.save()

        product_data = ProductSerializer(product, context={'request': request}).data
        product_data['average_rating'] = average_rating

        return Response(product_data)





class ProductListView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, product_slug=None): 
        product = Product.objects.filter(is_active=True)
        product_data = ProductListSerializer(product, many=True, context={'request': request}).data

        return Response(product_data)



class ProductCreateCommentView(APIView):
    permission_classes = [IsAuthenticated]  # Kullanıcı girişi zorunlu
    serializer_class = ProductReviewSerializer

    def post(self, request, product_id, *args, **kwargs):
        data = request.data.copy()
        
        data['product'] = product_id  
        data['user'] = request.user.id  
        
        serializer = ProductReviewSerializer(data=data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


class ProductGetCommentView(APIView):

    def get(self, request, product_id, *args, **kwargs):
        try:
            reviews = ProductReview.objects.filter(product_id=product_id).order_by('-created_at')
            serializer = ProductReviewSerializer(reviews, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ProductReview.DoesNotExist:
            return Response({"error": "Yorum bulunamadı."}, status=status.HTTP_404_NOT_FOUND)
        

class QuestionsGetView(APIView):
    permission_classes = [AllowAny]  
    serializer_class = QuestionSerializer

    def get(self, request, product_id, *args, **kwargs):
        try:
            questions = Question.objects.filter(product_id=product_id).order_by('-created_at')
            serializer = QuestionSerializer(questions, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Question.DoesNotExist:
            return Response({"error": "Soru bulunamadı."}, status=status.HTTP_404_NOT_FOUND)

class QuestionsCreateView(APIView):
    permission_classes = [IsAuthenticated]  
    serializer_class = QuestionCreateSerializer

    def post(self, request, product_id, *args, **kwargs):
        data = request.data.copy()
        
        data['product'] = product_id  
        data['user'] = request.user.id 
        
        serializer = QuestionCreateSerializer(data=data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




class AddToCartView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        product_id = request.data.get('product_id')
        quantity = request.data.get('quantity', 1)
        is_rental = request.data.get('is_rental', False)
        rental_price = request.data.get('rental_price')
        selling_price = request.data.get('selling_price')
        session_key = request.data.get('session_key')

        # Validation
        if not product_id:
            return Response(
                {"state": False, "messages": "Ürün ID'si zorunludur!"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Ürün kontrolü
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response(
                {"state": False, "messages": "Ürün bulunamadı!"},
                status=status.HTTP_404_NOT_FOUND
            )

        try:
            cart = Cart.get_or_create_cart(request, session_key=session_key)

            existing_cart_item = CartItem.objects.filter(
                cart=cart,
                product=product
            ).first()

            cart = Cart.get_or_create_cart(request, session_key=session_key)
            existing_cart_item = CartItem.objects.filter(
                cart=cart,
                product=product,
            ).first()
            if existing_cart_item:
                if existing_cart_item.is_rental != is_rental:  # Biri kiralık, diğeri satılıksa
                    existing_type = "kiralık" if existing_cart_item.is_rental else "satılık"
                    new_type = "kiralık" if is_rental else "satılık"
                    return Response(
                        {"state": False, "messages": f"Bu ürün zaten {existing_type} olarak sepette mevcut. {new_type} olarak ekleyemezsiniz!"},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                else:
                    return Response(
                        {"state": False, "messages": "Bu ürün zaten sepette mevcut!"},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                
            # Yeni sepet öğesi oluştur
            CartItem.objects.create(
                cart=cart,
                product=product,
                quantity=quantity,
                is_rental=is_rental,
                rental_price=rental_price,
                selling_price=selling_price
            )

            cart_data = CartSerializer(cart).data
            return Response(
                {"state": True, "messages": "Ürün sepete eklendi!", "cart": cart_data},
                status=status.HTTP_201_CREATED
            )

        except Exception as e:
            return Response(
                {"state": False, "messages": "Bir hata oluştu!", "error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )



class GetCartView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            session_key = request.data.get('session_key') 
            user = request.user if request.user.is_authenticated else None

            if not session_key:
                return Response({'detail': 'session_key is required'}, status=400)

            cart = Cart.get_or_create_cart(request, session_key)

            # Eğer kullanıcı giriş yaptıysa, sepeti kullanıcıya bağla
            if user and cart.user is None:
                cart.user = user
                cart.save()

            cart_data = CartSerializer(cart).data
            return Response({ "state": True, "cart": cart_data }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(
                { "state": False, "messages": f"Sepet verisi çekilirken bir sorun oluştu: {str(e)}" },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )



class RemoveFromCartView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        cart_item_id = request.data.get('cart_item_id')

        # Sepet öğesi var mı kontrolü
        try:
            cart_item = CartItem.objects.get(id=cart_item_id)
        except CartItem.DoesNotExist:
            return Response({ "state":False, 'messages': 'Sepette ürün bulunamadı!'}, status=status.HTTP_404_NOT_FOUND)

        cart_id = cart_item.cart_id
        cart_item.delete()

        # Silinen ürün sonrası sepet verisi
        cart = Cart.objects.filter(id=cart_id, order_completed=False).first()
        cart_data = CartSerializer(cart).data

        return Response({ "state":True, 'messages': 'Ürün Silindi', "cart": cart_data}, status=status.HTTP_200_OK)



class UpdateCartItemQuantityView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        cart_item_id = request.data.get('cart_item_id')
        quantity = request.data.get('quantity')
        
        # Giriş doğrulama
        if not cart_item_id or quantity is None:
            return Response(
                {"state": False, "messages": "Sepet öğesi ID'si ve yeni miktar gereklidir!"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            cart_item = CartItem.objects.get(id=cart_item_id)
        except CartItem.DoesNotExist:
            return Response(
                {"state": False, "messages": "Sepette ürün bulunamadı!"},
                status=status.HTTP_404_NOT_FOUND
            )

        # Miktar sıfırdan küçükse hata ver
        if quantity <= 0:
            return Response(
                {"state": False, "messages": "Miktar sıfırdan büyük olmalıdır!"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Miktarı güncelle
        cart_item.quantity = quantity
        cart_item.save()

        # Sepet verilerini serialize et
        cart = cart_item.cart
        cart_data = CartSerializer(cart).data

        return Response(
            {"state": True, "messages": "Ürün miktarı başarıyla güncellendi.", "cart": cart_data},
            status=status.HTTP_200_OK
        )
