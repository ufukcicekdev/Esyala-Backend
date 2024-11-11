# views.py

from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated,AllowAny
from customerauth.models import wishlist_model  
from customerauth.OrderProcess.orderserializers import *  
from main.serializers import *
from rest_framework import status



class OrderListAPIView(APIView):
    permission_classes = [AllowAny]  #TODO: düzeltilecek   
    serializer_class = OrderListSerializer()
    def get(self, request):
        order_list = Order.objects.filter(user=get_object_or_404(User, id=6)) #TODO: düzeltilecek
        serializer = OrderListSerializer(order_list, many=True)

        if not order_list.exists(): 
            return Response({
                'message': 'Sipariş Listesi Boş',
                'products': []
            }, status=204)  

        return Response({
            'order': serializer.data
        }, status=200)  
    

#TODO: order detail eklenecek    

