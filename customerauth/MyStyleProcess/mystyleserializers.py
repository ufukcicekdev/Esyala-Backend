from rest_framework import serializers
from customerauth.models import *
from rest_framework.generics import GenericAPIView
from drf_spectacular.utils import extend_schema_field


class RoomTypeListSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomType
        fields = ['id', 'name', 'image']  

class RoomTypePostSerializer(serializers.ModelSerializer):
    selected_room_type_id = serializers.IntegerField()

    class Meta:
        model = RoomType
        fields = ['selected_room_type_id'] 

    def validate_selected_room_type_id(self, value):
        if not value:
            raise serializers.ValidationError("Seçili alan boş bırakılamaz.")
        
        if not TimeRange.objects.filter(id=value).exists():
            raise serializers.ValidationError("Geçersiz bir alan seçildi.")
        
        return value

class HomeTypeListSerializer(serializers.ModelSerializer):
    class Meta:
        model = HomeType
        fields = ['id', 'name', 'image']  

class HomeTypePostSerializer(serializers.ModelSerializer):
    selected_home_type_id = serializers.IntegerField()
    class Meta:
        model = HomeType
        fields = ['selected_home_type_id']  

    def validate_selected_home_type_id(self, value):
        if not value:
            raise serializers.ValidationError("Seçili alan boş bırakılamaz.")
        
        if not TimeRange.objects.filter(id=value).exists():
            raise serializers.ValidationError("Geçersiz bir alan seçildi.")
        
        return value

class HomeModelListSerializer(serializers.ModelSerializer):
    class Meta:
        model = HomeModel
        fields = ['id', 'name', 'image']  

class HomeModelPostSerializer(serializers.ModelSerializer):
    selected_home_model_id = serializers.IntegerField()
    class Meta:
        model = HomeModel
        fields = ['selected_home_model_id']

    def validate_selected_home_model_id(self, value):
        if not value:
            raise serializers.ValidationError("Seçili alan boş bırakılamaz.")
        
        if not TimeRange.objects.filter(id=value).exists():
            raise serializers.ValidationError("Geçersiz bir alan seçildi.")

        return value

class SpaceDefinitionListSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpaceDefinition
        fields = ['id', 'name', 'image']    

class SpaceDefinitionPostSerializer(serializers.ModelSerializer):
    selected_space_def_id = serializers.IntegerField()
    class Meta:
        model = SpaceDefinition
        fields = ['selected_space_def_id']  

    def validate_selected_space_def_id(self, value):
        if not value:
            raise serializers.ValidationError("Seçili alan boş bırakılamaz.")
        
        if not TimeRange.objects.filter(id=value).exists():
            raise serializers.ValidationError("Geçersiz bir alan seçildi.")

        return value

class TimeRangeListSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimeRange
        fields = ['id', 'name', 'image']   

class TimeRangePostSerializer(serializers.ModelSerializer):
    selected_time_range_id = serializers.IntegerField()
    class Meta:
        model = TimeRange
        fields = ['selected_time_range_id'] 

    def validate_selected_time_range_id(self, value):
        if not value:
            raise serializers.ValidationError("Seçili alan boş bırakılamaz.")
        
        if not TimeRange.objects.filter(id=value).exists():
            raise serializers.ValidationError("Geçersiz bir alan seçildi.")

        return value



class RoomTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomType
        fields = "__all__"

class HomeTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = HomeType
        fields = "__all__"

class HomeModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = HomeModel
        fields = "__all__"

class SpaceDefSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpaceDefinition
        fields = "__all__"

class TimeRangeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimeRange
        fields = "__all__"



class MyStyleCategoryListSerializer(serializers.ModelSerializer):
    room_type_data = serializers.SerializerMethodField()
    home_type_data = serializers.SerializerMethodField()
    home_model_data = serializers.SerializerMethodField()
    space_definition_data = serializers.SerializerMethodField()
    time_range_data = serializers.SerializerMethodField()

    class Meta:
        model = MyStyles
        fields = ["room_type_data", "home_type_data", "home_model_data", "space_definition_data", "time_range_data"]
    
    @extend_schema_field(serializers.IntegerField) 
    def get_room_type_data(self, obj):
        return RoomTypeSerializer(obj.room_type).data if obj.room_type and obj.room_type.is_active else None
    @extend_schema_field(serializers.IntegerField) 
    def get_home_type_data(self, obj):
        return HomeTypeSerializer(obj.home_type).data if obj.home_type and obj.home_type.is_active else None
    @extend_schema_field(serializers.IntegerField) 
    def get_home_model_data(self, obj):
        return HomeModelSerializer(obj.home_model).data if obj.home_model and obj.home_model.is_active else None
    @extend_schema_field(serializers.IntegerField) 
    def get_space_definition_data(self, obj):
        return SpaceDefSerializer(obj.space_definition).data if obj.space_definition and obj.space_definition.is_active else None
    @extend_schema_field(serializers.IntegerField) 
    def get_time_range_data(self, obj):
        return TimeRangeSerializer(obj.time_range).data if obj.time_range and obj.time_range.is_active else None





