from django.urls import path,include
from .views import *


app_name = "main"

urlpatterns = [
    path("get_home_main_banner/", GetHomeMainBanner.as_view(), name='get_home_main_banner'),
    path("get_home_sub_banner/", GetHomeSubBanner.as_view(), name='get_home_sub_banner'),
    path("get_social_media_links/", GetSocialMediaLinks.as_view(), name='get_social_media_links'),
    path("create_contact_us/", CreateContactUs.as_view(), name='create_contact_us'),


    path('homepage_best_seller_products/', HomepageBestSellerProductsView.as_view(), name='homepage_best_seller_products'),
    path('homepage_featured_products/', HomepageFeaturedProductsView.as_view(), name='homepage_featured_products'),
    path('homepage_latest_products/', HomepageLatestProductsView.as_view(), name='homepage_latest_products'),




    # path('about/', GetAboutPage.as_view(), name='get_team_members'),
    path('get_category/', CategoryAPIView.as_view(), name='get_category'),
    path('get_footer_category/', FooterCategoryAPIView.as_view(), name='get_footer_category'),

    path('get_brand/', GetBrand.as_view(), name='get_brand'),

    path("category/<path:category_slugs>/", GetCategoryProductListView.as_view(), name="get_category_product_list"),
    path("productCategoryList/<path:category_slugs>/", GetProductCategoryListView.as_view(), name="get_category_product_list"),


    path("category/rental", RentalProductView.as_view(), name="rental_product_list_view"),
    path("category/sales", SalesProductView.as_view(), name="sales_product_list_view"),

    path('search/<str:query>/', ProductSearchView.as_view(), name='product_search'),
    path('subscribe/', SubscribeView.as_view(), name='subscribe'),
]



