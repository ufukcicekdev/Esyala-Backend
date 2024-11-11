from rest_framework import serializers
from customerauth.models import *
import re



class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ['id','address_type', 'username', 'usersurname', 'phone', 'city', 'region', 'neighborhood',
                  'address_name', 'address_line1', 'postal_code', 'firm_name', 'firm_taxcode', 'firm_tax_home']
        read_only_fields = ['user', 'is_default']

    def validate(self, data):
        action = self.context.get('action')

        if data.get('address_type') == 2:  
            required_fields = ['firm_name', 'firm_taxcode', 'firm_tax_home']
            missing_fields = [field for field in required_fields if not data.get(field)]
            if missing_fields:
                raise serializers.ValidationError(
                    {field: "Bu alan fatura adresi için gereklidir." for field in missing_fields}
                )
            
        else:
            required_fields = ['address_type', 'username', 'usersurname', 'phone', 'city', 'region', 'neighborhood',
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


    def validate_phone(self, value):
        if not re.match(r'^\+?[1-9]\d{1,14}$', value):
            raise serializers.ValidationError("Lütfen geçerli bir telefon numarası girin.")
        return value
    



