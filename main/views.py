from warnings import filters
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from rest_framework import viewsets
from .models import *
from customerauth.models import wishlist_model
from .serializers import *
from rest_framework.permissions import IsAuthenticated, AllowAny
from products.models import Product,ProductRentalPrice,ProductReview
from rest_framework.views import APIView
from django.core.cache import cache
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.exceptions import NotFound
from django.db.models import Q,Avg,Prefetch,Exists, OuterRef
from rest_framework.pagination import PageNumberPagination
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie
from django.utils.decorators import method_decorator
from slack_send_messages.send_messages import send_contact_message
from .filter import ProductFilter
from django_filters import rest_framework as filters
from django_filters.rest_framework import DjangoFilterBackend


@method_decorator(cache_page(60 * 60 * 12), name='dispatch')  # 6 saatlik cache
@method_decorator(vary_on_cookie, name='dispatch')  # Vary on cookie
class GetHomeMainBanner(APIView):
    serializer_class = HomeMainBannerSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        return HomeMainBanner.objects.filter(is_active=True)
    
    def get(self, request, *args, **kwargs):
        try:
            queryset = self.get_queryset()
            if not queryset.exists():
                message = 'Şu anda anasayfa görsellerine ulaşılmıyor.'
                tags = "success"
                return Response({
                    "status": True,
                    "messages": message
                }, status=status.HTTP_200_OK)

            serializer = self.serializer_class(queryset, many=True)
            return Response({
                "status": True,
                "data": serializer.data
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                "status": False,
                "messages": "Bir hata oluştu"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    

class GetHomeSubBanner(generics.ListAPIView):
    serializer_class = HomeSubBannerSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        return HomeSubBanner.objects.filter(is_active=True)
    
    def get(self, request, *args, **kwargs):
        try:
            queryset = self.get_queryset()
            if not queryset.exists():
                message = 'Şu anda anasayfa görsellerine ulaşılmıyor.'
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
class GetSocialMediaLinks(generics.ListAPIView):
    serializer_class = SocialMediaSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        return SocialMedia.objects.all()
    
    def get(self, request, *args, **kwargs):
        try:
            queryset = self.get_queryset()
            if not queryset.exists():
                message = 'Şu anda sosyal medya linklerine ulaşılmıyor.'
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
    

class CreateContactUs(generics.CreateAPIView):
    serializer_class = ContactUsSerializer
    permission_classes = [AllowAny]

    
    def post(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid():
                serializer.save()

                contact_data = {
                    'full_name': serializer.validated_data['full_name'],
                    'email': serializer.validated_data['email'],
                    'phone': serializer.validated_data['phone'],
                    'subject': serializer.validated_data['subject'],
                    'message': serializer.validated_data['message'],
                }
    
                send_contact_message(contact_data)
                return Response({'status':True, 'messages': 'Mesajınız başarılı bir şekilde gönderildi.'}, status=HTTP_200_OK)
            
            if serializer.errors:
                messages_list = []  
                for key, value in serializer.errors.items(): 
                    print(value)
                    messages_list.append(value)  
            return Response({"status": False, 'messages': messages_list}, status=HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({
                "status": False,
                "messages": [{'Bir hata oluştu: {}'.format(str(e)) }]
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# @method_decorator(cache_page(60 * 60 * 24), name='dispatch')  # 6 saatlik cache
# @method_decorator(vary_on_cookie, name='dispatch')  # Vary on cookie
# class GetAboutPage(generics.ListAPIView):
#     serializer_class = AboutPageSerializer
#     permission_classes = [AllowAny]

#     def get_queryset(self):
#         return TeamMembers.objects.all().order_by('id')
    
#     def get(self, request, *args, **kwargs):
#         try:
#             queryset = self.get_queryset()
#             if not queryset.exists():
#                 message = 'Şu anda hakkımızda sayfasına ulaşılmıyor.'
#                 tags = "success"
#                 return Response({
#                     "status": True,
#                     "messages": [{'message': message, 'tags': tags}]
#                 }, status=status.HTTP_200_OK)

#             serializer = self.serializer_class(queryset, many=True)
#             return Response({
#                 "status": True,
#                 "data": serializer.data
#             }, status=status.HTTP_200_OK)
#         except Exception as e:
#             return Response({
#                 "status": False,
#                 "messages": [{'message': 'Bir hata oluştu: {}'.format(str(e)), 'tags': 'error'}]
#             }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)




# @method_decorator(cache_page(60 * 60 * 6), name='dispatch')  # 6 saatlik cache
# @method_decorator(vary_on_cookie, name='dispatch')  # Vary on cookie
class CategoryAPIView(APIView):
    permission_classes = [AllowAny]
    def get(self, request, *args, **kwargs):
        try:
            header_categories = get_category()
            return Response({
                "status": True,
                "data": header_categories
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({
                "status": False,
                "messages": [{'message': 'Bir hata oluştu: {}'.format(str(e)), 'tags': 'error'}]
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@method_decorator(cache_page(60 * 60 * 6), name='dispatch')  # 6 saatlik cache
@method_decorator(vary_on_cookie, name='dispatch')  # Vary on cookie
class FooterCategoryAPIView(APIView):
    permission_classes = [AllowAny]
    def get(self, request, *args, **kwargs):
        try:
            footer_categories = get_footer_category()
            
            return Response({
                "status": True,
                "data": footer_categories
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({
                "status": False,
                "messages": [{'message': 'Bir hata oluştu: {}'.format(str(e)), 'tags': 'error'}]
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        


def get_footer_category():
    key = 'footer_categories_json'
    footer_categories_json = cache.get(key)
    if not footer_categories_json:
        main_categories = Category.objects.filter(parent=None, is_active=True)
        footer_categories_json = GetFooterCategorySerializer(main_categories, many=True).data
        cache.set(key, footer_categories_json, 60 * 60 * 6)
    return footer_categories_json


def get_category():
    key = 'main_categories_json'
    main_categories_json = cache.get(key)
    
    if not main_categories_json:
        main_categories = Category.objects.filter(parent=None, is_active=True).prefetch_related('children')
        main_categories_json = GetCategorySerializer(main_categories, many=True).data
        cache.set(key, main_categories_json, 60 * 60 * 6)
        
    return main_categories_json



    
@method_decorator(cache_page(60 * 60 * 6), name='dispatch')  # 6 saatlik cache
@method_decorator(vary_on_cookie, name='dispatch')  # Vary on cookie
class HomepageBestSellerProductsView(APIView):
    serializer_class = CategoryProductSerializers
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        try:
            key = 'homepage_best_seller_products'
            cached_products = cache.get(key)

            if cached_products:
                return Response(cached_products)
            
            best_seller_products = Product.objects.filter(
                is_active=True, best_seller=True
            ).prefetch_related('related_products')[:16]
            

            serialized_data = CategoryProductSerializers(best_seller_products, many=True).data
            cache.set(key, serialized_data, 60 * 60 * 6)  
            return Response({
                "status": True,
                "data": serialized_data
            }, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response({
                "status": False,
                "messages": "Bir hata oluştu"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@method_decorator(cache_page(60 * 60 * 6), name='dispatch')  # 6 saatlik cache
@method_decorator(vary_on_cookie, name='dispatch')  # Vary on cookie
class HomepageFeaturedProductsView(APIView):
    serializer_class = CategoryProductSerializers
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        try:
            key = 'homepage_featured_products'
            cached_products = cache.get(key)

            if cached_products:
                return Response(cached_products)

            featured_products = Product.objects.filter(
                is_active=True, is_featured=True
            ).prefetch_related('related_products')[:16]
            
            serialized_data = CategoryProductSerializers(featured_products, many=True).data
            cache.set(key, serialized_data, 60 * 60 * 6)  
            return Response({
                "status": True,
                "data": serialized_data
            }, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response({
                "status": False,
                "messages": "Bir hata oluştu"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@method_decorator(cache_page(60 * 60 * 6), name='dispatch')  # 6 saatlik cache
@method_decorator(vary_on_cookie, name='dispatch')  # Vary on cookie
class HomepageLatestProductsView(APIView):
    serializer_class = CategoryProductSerializers
    permission_classes = [AllowAny]
    def get(self, request, *args, **kwargs):
        try:
            key = 'homepage_latest_products'
            cached_products = cache.get(key)

            if cached_products:
                return Response(cached_products)

            latest_products = Product.objects.filter(
                is_active=True
            ).order_by('-created_at').prefetch_related('related_products')[:16]

            serialized_data = CategoryProductSerializers(latest_products, many=True).data
            cache.set(key, serialized_data, 60 * 60 * 6)  
            return Response({
                "status": True,
                "data": serialized_data
            }, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response({
                "status": False,
                "messages": [{'message': 'Bir hata oluştu: {}'.format(str(e)), 'tags': 'error'}]
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



@method_decorator(cache_page(60 * 60 * 6), name='dispatch')  # 6 saatlik cache
@method_decorator(vary_on_cookie, name='dispatch')  # Vary on cookie
class GetBrand(APIView):
    serializer_class = GetBrandSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        return Brand.objects.filter(is_active=True).exclude(image__isnull=True).exclude(image='')
    
    def get(self, request, *args, **kwargs):
        try:
            queryset = self.get_queryset()
            if not queryset.exists():
                message = 'Şu anda markalara ulaşılmıyor.'
                return Response({
                    "status": True,
                    "messages": message
                }, status=status.HTTP_200_OK)

            serializer = self.serializer_class(queryset, many=True)
            return Response({
                "status": True,
                "data": serializer.data
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                "status": False,
                "messages": "Bir hata oluştu"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    



@method_decorator(cache_page(60 * 60 * 12), name='dispatch')
@method_decorator(vary_on_cookie, name='dispatch')
class GetCategoryProductListView(generics.ListAPIView):
    serializer_class = CategoryProductSerializers
    permission_classes = [AllowAny]
    pagination_class = PageNumberPagination
    filter_backends = (DjangoFilterBackend,) 
    filterset_class = ProductFilter 
    def get_queryset(self):
        category_slug = self.kwargs.get('category_slugs')
        # Kategoriye bağlı ürünler
        category_slug_list = category_slug.split('/')
        main_category = get_object_or_404(Category, slug=category_slug_list[0])

        if len(category_slug_list) == 1:
            # Ana kategori altındaki tüm ürünler
            queryset = Product.objects.filter(
                category__in=main_category.children.all(),
                is_active=True
            ).select_related('category').order_by('id')
        else:
            # Hedef kategoriye bağlı ürünler
            target_category = get_object_or_404(Category, slug=category_slug_list[-1])
            queryset = Product.objects.filter(
                category=target_category,
                is_active=True
            ).select_related('category').order_by('id')

        # Apply the filter
        queryset = ProductFilter(self.request.GET, queryset=queryset).qs

        return queryset

    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()  # Filtrelenmiş ürünleri alıyoruz
        page = self.paginate_queryset(queryset)

        product_count = queryset.count()

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response({
                "status": True,
                "data": {
                    "product": serializer.data,
                    "product_count": product_count,
                    "pagination": {
                        "next": self.paginator.get_next_link(),
                        "previous": self.paginator.get_previous_link(),
                        "page": request.query_params.get('page', 1),
                        "total_pages": self.paginator.page.paginator.num_pages,
                    },
                }
            })

        serializer = self.get_serializer(queryset, many=True)
        return Response({
            "status": True,
            "data": {
                "product": serializer.data,
                "product_count": product_count,
            }
        }, status=status.HTTP_200_OK)



@method_decorator(cache_page(60 * 60 * 6), name='dispatch')
@method_decorator(vary_on_cookie, name='dispatch')
class GetProductCategoryListView(generics.ListAPIView):
    serializer_class = CategoryProductSerializers
    permission_classes = [AllowAny]


    def get_queryset(self):
        category_slug = self.kwargs.get('category_slugs', '')
        # if not category_slug:
        #     return Category.objects.none()  # Hiçbir şey döndürme

        category_slug_list = category_slug.split('/')
        main_category = get_object_or_404(Category, slug=category_slug_list[0])

        if len(category_slug_list) == 1:
            return main_category.children.all()
        else:
            target_category = get_object_or_404(Category, slug=category_slug_list[-1])
            return target_category.product_set.all()

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        breadcrumb_categories, subcategories = self.get_breadcrumb_and_subcategories()

        response_data = {
            "status": True,
            "data": {
                "category": {
                    "breadcrumb": breadcrumb_categories,
                    "subcategories": [
                        {"name": sub.name, "slug": sub.slug} for sub in subcategories
                    ],
                },
            }
        }

        return Response(response_data, status=status.HTTP_200_OK)

    def get_breadcrumb_and_subcategories(self):
        category_slug = self.kwargs.get('category_slugs', '')
        breadcrumb_categories = []
        subcategories = []

        if category_slug == 'rental':
            breadcrumb_categories = [{
                "name": "Kiralık Ürünler",
                "slug": "rental"
            }]
        else:
            category_slug_list = category_slug.split('/')
            main_category = get_object_or_404(Category, slug=category_slug_list[0])

            breadcrumb_categories.append({
                "name": main_category.name,
                "slug": main_category.slug
            })
            subcategories = main_category.children.all()

            for slug in category_slug_list[1:]:
                category = get_object_or_404(Category, slug=slug)
                breadcrumb_categories.append({
                    "name": category.name,
                    "slug": category.slug
                })

        return breadcrumb_categories, subcategories
 






class ProductSearchView(APIView):
    permission_classes = [AllowAny]
    def get(self, request, query, format=None):
        try:
            if query:
                query_terms = query.split()

                search_criteria = Q(is_active=True)

                for term in query_terms:
                    search_criteria &= (
                        Q(name__icontains=term) |
                        Q(description__icontains=term) |
                        Q(information__icontains=term)
                    )

                products = Product.objects.filter(search_criteria).order_by('id')

                if products:
                    categories = {product.category.id: product.category for product in products}  
                    category_list = list(categories.values())  

                    serializer = CategoryProductSerializers(products, many=True)
                    
                    data ={
                        "products": serializer.data,
                        "categories": ProductWithCategoriesSerializer(category_list, many=True).data  
                    }
                
                    return Response({
                        "status": True,
                        "data": data
                    }, status=status.HTTP_200_OK)
                

                message = 'Ürün Bulunmadı!'
                tags = "success"
                return Response({
                    "status": True,
                    "messages": [{'message': message, 'tags': tags}]
                }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                "status": False,
                "messages": [{'message': 'Bir hata oluştu: {}'.format(str(e)), 'tags': 'error'}]
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class SubscribeView(APIView):
    serializer_class = SubscriptionSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            serializer = SubscriptionSerializer(data=request.data)
            if serializer.is_valid(): 
                email = serializer.validated_data['email']  
                subscription, created = Subscription.objects.get_or_create(email=email)
                if created:
                    return Response({ "status": True, "messages": "Abonelik işlemi başarıyla tamamlandı."}, status=status.HTTP_201_CREATED)
                else:
                    return Response({ "status": False, "messages": "Bu e-posta adresi zaten kayıtlı."}, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({
                "status": False,
                "messages": [{'message': 'Bir hata oluştu: {}'.format(str(e)), 'tags': 'error'}]
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

class RentalProductView(APIView):
    permission_classes = [AllowAny]
    def get(self, request, format=None):
        try:
            products = Product.objects.filter(
            is_active=True
                ).annotate(
                    has_rental_price=Exists(ProductRentalPrice.objects.filter(product=OuterRef('pk')))
                ).filter(
                    has_rental_price=True  
                ).select_related('category').prefetch_related(
                    Prefetch('related_products', queryset=ProductImage.objects.all()),
                    Prefetch('reviews', queryset=ProductReview.objects.all()),
                    Prefetch('wishes', queryset=wishlist_model.objects.all())
                ).annotate(average_rating=Avg('reviews__rating')).order_by('id')
            
            if products:
                categories = {product.category.id: product.category for product in products}  
                category_list = list(categories.values())  
                serializer = CategoryProductSerializers(products, many=True)
                data ={
                    "products": serializer.data,
                    "categories": ProductWithCategoriesSerializer(category_list, many=True).data  
                }
                return Response({
                    "status": True,
                    "data": data
                }, status=status.HTTP_200_OK)

            message = 'Ürün Bulunmadı!'
            tags = "success"
            return Response({
                "status": True,
                "messages": [{'message': message, 'tags': tags}]
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                "status": False,
                "messages": [{'message': 'Bir hata oluştu: {}'.format(str(e)), 'tags': 'error'}]
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

class SalesProductView(APIView):
    permission_classes = [AllowAny]
    def get(self, request, format=None):
        try:
            products = Product.objects.filter(
            is_active=True
            ).select_related('category').prefetch_related(
                Prefetch('related_products', queryset=ProductImage.objects.all()),
                Prefetch('reviews', queryset=ProductReview.objects.all()),
                Prefetch('wishes', queryset=wishlist_model.objects.all())
            ).annotate(average_rating=Avg('reviews__rating')).order_by('id')
                
            if products:
                categories = {product.category.id: product.category for product in products}  
                category_list = list(categories.values())  

                serializer = CategoryProductSerializers(products, many=True)
                
                data = {
                    "products": serializer.data,
                    "categories": ProductWithCategoriesSerializer(category_list, many=True).data  
                }
                return Response({
                    "status": True,
                    "data": data
                }, status=status.HTTP_200_OK)
            
            message = 'Ürün Bulunmadı!'
            tags = "success"
            return Response({
                "status": True,
                "messages": [{'message': message, 'tags': tags}]
            }, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response({
                "status": False,
                "messages": [{'message': 'Bir hata oluştu: {}'.format(str(e)), 'tags': 'error'}]
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
