# views.py

from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated,AllowAny
from customerauth.models import wishlist_model  
from customerauth.WishlistProcess.wishlistleserializers import *  
from main.serializers import *
from rest_framework import status

class WishlistAPIView(APIView):
    permission_classes = [AllowAny]  
    serializer_class = WishlistProductSerializer()
    def get(self, request):
        wishlist_products = wishlist_model.objects.filter(user=get_object_or_404(User, id=1)) #TODO: düzeltilecek
        print("wishlist_products",wishlist_products)
        serializer = WishlistProductSerializer(wishlist_products, many=True)

        if not wishlist_products.exists(): 
            return Response({
                'message': 'Beğeni Listesi Boş',
                'products': []
            }, status=204)  

        return Response({
            'products': serializer.data
        }, status=200)  



class AddToWishlistAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, product_id):
        messages_list = []

        try:
            product = Product.objects.get(id=product_id)

            wishlist_item, created = wishlist_model.objects.get_or_create(product=product, user=get_object_or_404(User, id=1))#TODO:düzeltilecek
            wishlist_count = wishlist_model.objects.filter(user=get_object_or_404(User, id=1)).count() #TODO:düzeltilecek

            if created:
                message = 'Ürün listenize eklendi!'
                tags = "success"
                messages_list.append({'message': message, 'tags': tags})
                return Response({
                    "status": True,
                    "wishlist_count": wishlist_count,
                    "messages": messages_list
                }, status=status.HTTP_201_CREATED)
            else:
                message = 'Ürün zaten beğeni listenizde bulunuyor!'
                tags = "warning"
                messages_list.append({'message': message, 'tags': tags})
                return Response({
                    "status": True,
                    "wishlist_count": wishlist_count,
                    "messages": messages_list
                }, status=status.HTTP_200_OK)

        except Exception as e:
            message = 'Ürün eklenirken bir sorun oluştu!'
            tags = "error"
            messages_list.append({'message': message, 'tags': tags})
            return Response({
                "status": False,
                "wishlist_count": 0,
                "messages": messages_list
            }, status=status.HTTP_400_BAD_REQUEST)
        


class RemoveFromWishlistAPIView(APIView):
    permission_classes = [AllowAny]

    def delete(self, request, wish_id):
        messages_list = []
        try:
            wishlist_item = get_object_or_404(wishlist_model, id=wish_id, user=get_object_or_404(User, id=1)) #TODO:düzeltilecek
            wishlist_item.delete()
            message = 'Ürün listenizden başarıyla kaldırıldı!'
            tags = "success"
            messages_list.append({'message': message, 'tags': tags})

            return Response({
                "status": True,
                "messages": messages_list
            }, status=status.HTTP_200_OK)

        except wishlist_model.DoesNotExist:
            message = 'Ürün bulunamadı veya silinemedi!'
            tags = "error"
            messages_list.append({'message': message, 'tags': tags})
            return Response({
                "status": False,
                "messages": messages_list
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            message = 'Bir hata oluştu!'
            tags = "error"
            messages_list.append({'message': message, 'tags': tags})
            return Response({
                "status": False,
                "messages": messages_list
            }, status=status.HTTP_400_BAD_REQUEST)