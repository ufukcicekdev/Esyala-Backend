from rest_framework import status
from rest_framework.decorators import APIView
from rest_framework.response import Response
from rest_framework import generics
from rest_framework.permissions import AllowAny
from customerauth.CityProcess.cityserializers import *



class GetCityAPIView(generics.ListAPIView):
    permission_classes = [AllowAny]  #TODO: düzetilecek
    serializer_class = CitySerializer

    def get_queryset(self):
        return City.objects.filter(city_id=34)  #Sadece istabul gelecek
    


class GetDistrictAPIView(APIView):
    permission_classes = [AllowAny]  # TODO: düzetilecek
    serializer_class = DistricstSerializer

    def get(self, request, city_id):
        filter_district = District.objects.filter(city_id=city_id)
        
        if not filter_district.exists():
            return Response({"detail": "Bu şehre ait ilçe bulunmamaktadır."}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = DistricstSerializer(filter_district, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK) 
    

class GetNeighborhoodAPIView(APIView):
    permission_classes = [AllowAny]  # TODO: düzetilecek
    serializer_class = NeighborhoodSerializer
    def get(self, request, district_id):
        filter_district = Neighborhood.objects.filter(district_id=district_id)
        
        if not filter_district.exists():
            return Response({"detail": "Bu şehre ait mahalle bulunmamaktadır."}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = NeighborhoodSerializer(filter_district, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK) 