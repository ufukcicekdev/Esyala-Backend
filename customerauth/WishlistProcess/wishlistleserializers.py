# serializers.py

from rest_framework import serializers
from customerauth.models import *
from main.serializers import *


class WishlistProductSerializer(serializers.ModelSerializer):
    product = CategoryProductSerializers()  # Product bilgilerini serileştirmek için

    class Meta:
        model = wishlist_model
        fields = ['id', 'product', 'date']  # İlgili alanları ekleyin
