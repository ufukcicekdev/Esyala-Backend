from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from rest_framework.exceptions import NotFound
from rest_framework.permissions import AllowAny
from .serializers import GetBlogsSerializer, GetBlogCategorySerializer, GetBlogDetailSerializer
from blog.models import Blog, Category
from rest_framework.views import APIView
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie
from django.utils.decorators import method_decorator

@method_decorator(cache_page(60 * 60 * 6), name='dispatch')  # 6 saatlik cache
@method_decorator(vary_on_cookie, name='dispatch')  # Vary on cookie
class GetBlogsView(APIView):
    serializer_class = GetBlogsSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        return Blog.objects.filter(is_active=True)

    def get(self, request, *args, **kwargs):
        try:    
            queryset = self.get_queryset()
            if not queryset.exists():
                message = 'Şu anda görüntüleyebileceğiniz aktif blog içeriği bulunmamaktadır.'
                tags = "success"
                return Response({
                    "status": True,
                    "messages": [{'message': message, 'tags': tags}]
                }, status=status.HTTP_200_OK)

            serializer = self.serializer_class(queryset, many=True)
            return Response({
                "status": True,
                "data": serializer.data
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                "status": False,
                "messages": [{'message': 'Bir hata oluştu: {}'.format(str(e)), 'tags': 'error'}]
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



@method_decorator(cache_page(60 * 60 * 6), name='dispatch')  # 6 saatlik cache
@method_decorator(vary_on_cookie, name='dispatch')  # Vary on cookie
class GetPopularBlogsViews(APIView):
    serializer_class = GetBlogsSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        return Blog.objects.filter(is_active=True, views__gt=10).order_by('-created_at')
    
    def get(self, request, *args, **kwargs):
        try:
            queryset = self.get_queryset()
            if not queryset.exists():
                message = 'Şu anda görüntüleyebileceğiniz popüler blog içeriği bulunmamaktadır.'
                tags = "success"
                return Response({
                    "status": True,
                    "messages": [{'message': message, 'tags': tags}]
                }, status=status.HTTP_200_OK)

            serializer = self.serializer_class(queryset, many=True)
            return Response({
                "status": True,
                "data": serializer.data
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                "status": False,
                "messages": [{'message': 'Bir hata oluştu: {}'.format(str(e)), 'tags': 'error'}]
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

@method_decorator(cache_page(60 * 60 * 6), name='dispatch')  # 6 saatlik cache
@method_decorator(vary_on_cookie, name='dispatch')  # Vary on cookie
class GetBlogsCategoriesView(APIView):
    serializer_class = GetBlogCategorySerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        return Category.objects.filter(is_active=True)
        
    def get(self, request, *args, **kwargs):
        try:
            queryset = self.get_queryset()
            if not queryset.exists():
                message = 'Şu anda görüntüleyebileceğiniz aktif kategori bulunmamaktadır.'
                tags = "success"
                return Response({
                    "status": True,
                    "messages": [{'message': message, 'tags': tags}]
                }, status=status.HTTP_200_OK)

            serializer = self.serializer_class(queryset, many=True)
            return Response({
                "status": True,
                "data": serializer.data
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                "status": False,
                "messages": [{'message': 'Bir hata oluştu: {}'.format(str(e)), 'tags': 'error'}]
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



@method_decorator(cache_page(60 * 60 * 6), name='dispatch')  # 6 saatlik cache
@method_decorator(vary_on_cookie, name='dispatch')  # Vary on cookie
class GetBlogDetailViews(APIView):
    serializer_class = GetBlogDetailSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        blog_slug = self.kwargs.get('slug')
        return Blog.objects.filter(slug=blog_slug, is_active=True)

    def get(self, request, *args, **kwargs):
        try:
            queryset = self.get_queryset()
            blog = queryset.first()  # İlk bloğu alıyoruz

            if not blog:  # Blog bulunamadıysa
                message = 'Şu anda ilgili bloğa erişilemiyor, blog silinmiş olabilir.'
                return Response({
                    "status": False,
                    "messages": [{'message': message, 'tags': 'error'}]
                }, status=status.HTTP_404_NOT_FOUND)

     
            blog.views += 1
            blog.save()

            # Blog'u serileştir ve döndür
            serializer = self.serializer_class(blog)  # Tek bir nesne için many=False
            return Response({
                "status": True,
                "data": serializer.data
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({
                "status": False,
                "messages": [{'message': 'Bir hata oluştu: {}'.format(str(e)), 'tags': 'error'}]
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)





@method_decorator(cache_page(60 * 60 * 6), name='dispatch')  # 6 saatlik cache
@method_decorator(vary_on_cookie, name='dispatch')  # Vary on cookie
class GetCategoryBlogsViews(generics.ListAPIView):
    serializer_class = GetBlogsSerializer  
    permission_classes = [AllowAny]

    def get_queryset(self):
        category_slug = self.kwargs.get('slug')
        category = get_object_or_404(Category, slug=category_slug, is_active=True)
        return Blog.objects.filter(category=category, is_active=True)
        
    def get(self, request, *args, **kwargs):
        try:
            queryset = self.get_queryset()
            if not queryset.exists():
                message = 'Şu anda ilgili kategorideki bloglara erişilmiyor.'
                tags = "success"
                return Response({
                    "status": True,
                    "messages": [{'message': message, 'tags': tags}]
                }, status=status.HTTP_200_OK)

            serializer = self.serializer_class(queryset, many=True)
            return Response({
                "status": True,
                "data": serializer.data
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                "status": False,
                "messages": [{'message': 'Bir hata oluştu: {}'.format(str(e)), 'tags': 'error'}]
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)