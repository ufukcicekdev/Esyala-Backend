from rest_framework import serializers
from .models  import *
from django.core.exceptions import ValidationError
from rest_framework.generics import RetrieveAPIView
from drf_spectacular.utils import extend_schema_field



class GetBlogCategorySerializer(serializers.ModelSerializer):
    class Meta():
        model = Category
        fields = ["name", "slug"]


class GetBlogsSerializer(serializers.ModelSerializer):
    category = GetBlogCategorySerializer()
    created_at = serializers.DateTimeField(format="%Y-%m-%d", read_only=True) 
    class Meta():
        model = Blog
        fields = ["category", "title", "short_description", "banner", "slug", "created_at", "views"]
    
    @extend_schema_field(serializers.CharField) 
    def get_categories(self, obj):
        active_categories = obj.category.filter(is_active=True)
        return GetBlogCategorySerializer(active_categories, many=True).data




class GetBlogDetailSerializer(serializers.ModelSerializer):
    category = serializers.SerializerMethodField()

    class Meta:
        model = Blog
        fields = ["category", "title", "description", "banner", "slug", "created_at", "views"]

    @extend_schema_field(serializers.CharField) 
    def get_category(self, obj):
        if obj.category.is_active: 
            return GetBlogCategorySerializer(obj.category).data
        return None