from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import APIView
from rest_framework.response import Response
from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from customerauth.models import *
from customerauth.AddressProcess.addressSerializers import *


class AddressListView(APIView):
    permission_classes = [AllowAny]  #TODO: düzetilecek
    serializer_class = AddressListSerializer
    def get(self, request):
        addresses = Address.objects.filter(user=get_object_or_404(User, id=6))  #TODO: düzetilecek
        serializer = AddressListSerializer(addresses, many=True, context={'request': request, 'action': 'list'})
        return Response({"status": True, "address":serializer.data}, status=status.HTTP_200_OK)


class AddressCreateView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AddressSerializer

    def post(self, request):
        serializer = AddressSerializer(data=request.data, context={'request': request, 'action': 'create'})
        
        if serializer.is_valid():
            address_model = serializer.validated_data.get('address_model')

            # address_type için doğru tipte kontrol yapalım
            if address_model == 2:
                Address.objects.filter(user=request.user, delivery_addresses=True).update(is_default=False)
            elif address_model == 1:
                Address.objects.filter(user=request.user, billing_addresses=True).update(is_default=False)

            new_address = serializer.save(user=request.user)

            # address_type'in 'delivery' veya 'billing' olması durumunda uygun ayarları yapıyoruz
            if address_model ==  2:
                new_address.delivery_addresses = True
                new_address.billing_addresses = False
                new_address.is_default = True
            elif address_model == 1:
                new_address.delivery_addresses = False
                new_address.billing_addresses = True
                new_address.is_default = True

            new_address.save()

            # Serializer ile veri döndürüyoruz
            return Response(AddressSerializer(new_address).data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AddressUpdateView(APIView):
    permission_classes = [AllowAny]  #TODO: düzetilecek
    serializer_class = AddressSerializer
    def put(self, request, address_id):
        address = get_object_or_404(Address, id=address_id, user=request.user)
        serializer = AddressSerializer(address, data=request.data, partial=True, context={'request': request, 'action': 'update'})
        if serializer.is_valid():

            address_type = serializer.validated_data.get('address_type')

            if address_type == 'delivery':
                Address.objects.filter(user=request.user, delivery_addresses=True).update(is_default=False)
            elif address_type == 'billing':
                Address.objects.filter(user=request.user, billing_addresses=True).update(is_default=False)

            if address_type == 'delivery':
                address.delivery_addresses = True
                address.billing_addresses = False
                address.is_default = True
            elif address_type == 'billing':
                address.delivery_addresses = False
                address.billing_addresses = True
                address.is_default = True

            serializer.save()
            return Response({"status": True, "address":serializer.data}, status=status.HTTP_200_OK)
        return Response({"status": False, "message":serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    
class DeleteAddressView(APIView):
    permission_classes = [IsAuthenticated] 

    def delete(self, request, address_id):
        address = Address.objects.filter(id=address_id, user=request.user).first()

        if not address:
            return Response({
                "status": False,
                "message": "Adres silinirken bir sorun oluştu!"
            }, status=status.HTTP_404_NOT_FOUND)

        address.delete()

        return Response({
            "status": True,
            "message": "Adres başarıyla silindi."
        }, status=status.HTTP_200_OK)
