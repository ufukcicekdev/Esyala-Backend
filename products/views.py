from datetime import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import Product, ProductReview
from .serializers import ProductSerializer
from customerauth.models import UserProductView
from django.shortcuts import get_object_or_404
from django.db.models import Avg


class ProductDetailView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, product_slug):
        product = get_object_or_404(Product, slug=product_slug, is_active=True)
        
        reviews = ProductReview.objects.filter(product=product)
        
        average_rating = int(reviews.aggregate(Avg('rating'))['rating__avg'] or 0)

        # Kullanıcı login ise, UserProductView'e kaydetme
        if request.user.is_authenticated:
            user_product_view, created = UserProductView.objects.get_or_create(user=request.user, product=product)
            if not created:
                user_product_view.created_date = timezone.now()
                user_product_view.save()

        product_data = ProductSerializer(product, context={'request': request}).data
        product_data['average_rating'] = average_rating
        
        return Response(product_data)
