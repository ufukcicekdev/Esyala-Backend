from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from customerauth.models import Order 
from customerauth.OrderProcess.orderserializers import OrderDetailSerializer, OrderListSerializer
from rest_framework import status

class OrderListAPIView(APIView):
    permission_classes = [IsAuthenticated]  

    def get(self, request, *args, **kwargs):
        try:   
            order_list = Order.objects.filter(user=request.user)

            if not order_list.exists():
                return Response({
                    "status": True,
                    "message": "Sipariş Listesi Boş",
                }, status=status.HTTP_204_NO_CONTENT)

            serializer = OrderListSerializer(order_list, many=True)

            return Response({
                "status": True,
                "orders": serializer.data  
            }, status=status.HTTP_200_OK)
        except:
            return Response({
                "status": False,
                "message": "Bir sorun oluştu!"
            }, status=status.HTTP_400_BAD_REQUEST)

    


class OrderDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]  

    def get(self, request, order_number, *args, **kwargs):
        try:
            order_list = Order.objects.filter(user=request.user, order_number=order_number)

            if not order_list.exists():
                return Response({
                    "status": True,
                    "message": "Sipariş Listesi Boş",
                }, status=status.HTTP_204_NO_CONTENT)

            serializer = OrderDetailSerializer(order_list, many=True)

            return Response({
                "status": True,
                "orders": serializer.data  
            }, status=status.HTTP_200_OK)
        except:
            return Response({
                "status": False,
                "message": "Bir sorun oluştu!"
            }, status=status.HTTP_400_BAD_REQUEST)
