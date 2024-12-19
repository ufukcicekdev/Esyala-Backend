from django.urls import path,include
from .views import *

app_name = "products"


urlpatterns = [
    path('api/products/<slug:product_slug>/', ProductDetailView.as_view(), name='product_detail_api'),
    path('api/product_get_comment/<int:product_id>/', ProductGetCommentView.as_view(), name='product_get_comment_api'),
    path('api/product_create_comment/<int:product_id>/', ProductCreateCommentView.as_view(), name='product_create_comment_api'),


    path('api/product_get_questions/<int:product_id>/', QuestionsGetView.as_view(), name='product_get_questions_api'),
    path('api/product_create_question/<int:product_id>/', QuestionsCreateView.as_view(), name='product_create_questions_api'),



    path('api/product/cart/', GetCartView.as_view(), name='get-cart'),  
    path('api/product/cart/add/', AddToCartView.as_view(), name='add-to-cart'), 
    path('api/product/remove/', RemoveFromCartView.as_view(), name='remove-from-cart'),
    path('api/product/update_quantity/', UpdateCartItemQuantityView.as_view(), name='update_cart_item_quantity'),

    path('api/productsList/', ProductListView.as_view(), name='product_list_api'),

]

