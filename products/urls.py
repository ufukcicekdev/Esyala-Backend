from django.urls import path,include
from .views import *

app_name = "products"


urlpatterns = [
    path('api/products/<slug:product_slug>/', ProductDetailView.as_view(), name='product_detail_api'),
    path('api/productsList/', ProductListView.as_view(), name='product_list_api'),

]

