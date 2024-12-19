from rest_framework import serializers
from customerauth.models import *
import re

from customerauth.serializers import CitySerializer, DistrictdSerializer, NeighborhoodSerializer



class AddressListSerializer(serializers.ModelSerializer):
    city = CitySerializer()
    neighborhood = NeighborhoodSerializer()
    region = DistrictdSerializer()
    class Meta:
        model = Address
        fields = ['id','address_type', 'address_model', 'username', 'usersurname', 'phone', 'city', 'region', 'neighborhood',
                  'address_name', 'address_line1', 'postal_code', 'firm_name', 'firm_taxcode', 'firm_tax_home','is_default']





class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ['id','address_type','address_model', 'username', 'usersurname', 'phone', 'city', 'region', 'neighborhood',
                  'address_name', 'address_line1', 'postal_code', 'firm_name', 'firm_taxcode', 'firm_tax_home', 'is_default']
        read_only_fields = ['user', 'is_default']

    def validate(self, data):
        action = self.context.get('action')
        address_type = data.get('address_type')

        # Kurumsal adres için zorunlu alanlar
        if address_type == 2:  # Kurumsal adres
            required_fields = ['firm_name', 'firm_taxcode', 'firm_tax_home']
            missing_fields = [field for field in required_fields if not data.get(field)]
            if missing_fields:
                raise serializers.ValidationError(
                    {field: "Bu alan fatura adresi için gereklidir." for field in missing_fields}
                )
        
        # Bireysel adres için zorunlu alanlar
        elif address_type == 1:  # Bireysel adres
            required_fields = ['address_type', 'address_model', 'username', 'usersurname', 'phone', 'city', 'region', 'neighborhood',
                               'address_name', 'address_line1']
            missing_fields = [field for field in required_fields if not data.get(field)]
            if missing_fields:
                raise serializers.ValidationError(
                    {field: "Bu alan bireysel adres için gereklidir." for field in missing_fields}
                )

        if action == 'create':
            if data.get('is_default') and Address.objects.filter(user=self.context['request'].user, is_default=True).exists():
                raise serializers.ValidationError("Zaten bir varsayılan adresiniz mevcut.")
        
        elif action == 'update':
            if data.get('billing_addresses') and data.get('delivery_addresses'):
                raise serializers.ValidationError("Bir adres hem teslimat hem de fatura adresi olarak işaretlenemez.")
        
        return data
