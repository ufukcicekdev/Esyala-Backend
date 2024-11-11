# serializers.py

from rest_framework import serializers
from customerauth.models import *
from main.serializers import *


class OrderItemListSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = "__all__"



class OrderListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = "__all__"



class OrderListSerializer(serializers.ModelSerializer):
    orderItem = OrderItemListSerializer()
    class Meta:
        model = Order
        fields = ["orderItem"]
