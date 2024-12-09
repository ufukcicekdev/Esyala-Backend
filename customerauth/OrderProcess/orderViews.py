from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from customerauth.models import Order 
from customerauth.OrderProcess.orderserializers import OrderDetailSerializer, OrderListSerializer
from rest_framework import status

class OrderListAPIView(APIView):
    permission_classes = [IsAuthenticated]  

    def get(self, request, user_id, *args, **kwargs):
        order_list = Order.objects.filter(user=user_id)

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
    


class OrderDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]  

    def get(self, request, user_id, order_number, *args, **kwargs):
        order_list = Order.objects.filter(user=user_id, order_number=order_number)

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

