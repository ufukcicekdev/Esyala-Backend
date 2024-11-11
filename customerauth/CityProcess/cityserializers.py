from rest_framework import serializers
from customerauth.models import *
import re




class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = "__all__"

class DistricstSerializer(serializers.ModelSerializer):
    class Meta:
        model = District
        fields = "__all__"

class NeighborhoodSerializer(serializers.ModelSerializer):
    class Meta:
        model = Neighborhood
        fields = "__all__"