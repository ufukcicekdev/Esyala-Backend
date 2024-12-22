from rest_framework import status
from rest_framework.decorators import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from customerauth.CityProcess.cityserializers import *
from customerauth.models import City, District, Neighborhood

class GetCityAPIView(APIView):
    permission_classes = [AllowAny]  
    serializer_class = CitySerializer

    def get(self, request):
        try:
            city = City.objects.filter(city_id=34).first()
            if city:
                serializer = CitySerializer(city)
                return Response({
                    "status": "success",
                    "message": "Şehir başarıyla getirildi.",
                    "data": serializer.data
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    "status": "error",
                    "message": "İstanbul bulunamadı."
                }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({
                "status": "error",
                "message": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class GetDistrictAPIView(APIView):
    permission_classes = [AllowAny]  
    serializer_class = DistricstSerializer

    def get(self, request, city_id):
        try:
            filter_district = District.objects.filter(city_id=city_id)

            if not filter_district.exists():
                return Response({
                    "status": "error",
                    "message": "Bu şehre ait ilçe bulunmamaktadır."
                }, status=status.HTTP_404_NOT_FOUND)

            serializer = DistricstSerializer(filter_district, many=True)
            return Response({
                "status": "success",
                "message": "İlçeler başarıyla getirildi.",
                "data": serializer.data
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({
                "status": "error",
                "message": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class GetNeighborhoodAPIView(APIView):
    permission_classes = [AllowAny] 
    serializer_class = NeighborhoodSerializer

    def get(self, request, district_id):
        try:
            filter_district = Neighborhood.objects.filter(district_id=district_id)

            if not filter_district.exists():
                return Response({
                    "status": "error",
                    "message": "Bu ilçeye ait mahalle bulunmamaktadır."
                }, status=status.HTTP_404_NOT_FOUND)

            serializer = NeighborhoodSerializer(filter_district, many=True)
            return Response({
                "status": "success",
                "message": "Mahalleler başarıyla getirildi.",
                "data": serializer.data
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({
                "status": "error",
                "message": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)




