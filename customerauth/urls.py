from django.urls import path,include,re_path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import *
from .AddressProcess.addressViews  import *
from .CityProcess.cityViews import *
from .MyStyleProcess.mystyleViews import *
from .WishlistProcess.wishlistViews import *
from .OrderProcess.orderViews import *


urlpatterns = [
    path('user/token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('user/auth/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('user/token/refresh/', CustomTokenRefreshView.as_view(), name='token_refresh'),
    path('user/register/', UserRegistrationView.as_view(), name='auth_register'),
    path('user/login/',UserLoginView.as_view(),name="login"),
    path('user/logout/', LogoutView.as_view(), name='logout'),
    path('user/verify/<uidb64>/<token>/', VerifyEmailView.as_view(), name='verify_email'),



    path('user/password-reset-request/', PasswordResetRequestAPIView.as_view(), name='password_reset_request_api'),
    path('user/password-reset-verify/', PasswordResetVerifyAPIView.as_view(), name='password_reset_verify_api'),
    path('user/password-reset-change-password/', PasswordResetChangePasswordAPIView.as_view(), name='password_reset_verify_api'),


    #UserProfile
    path('user/profile/', ProfileAPIView.as_view(), name='profile_view'),
    path('user/profile/update/', ProfileUpdateAPIView.as_view(), name='profile_update'),
    path('user/password-change/', PasswordChangeView.as_view(), name='password_change'),
    path('user/change-email/', ChangeEmailAPIView.as_view(), name='change_email'),

    #Address Prcessing
    path('user/addresses/', AddressListView.as_view(), name='address_list'),
    path('user/addresses/create/', AddressCreateView.as_view(), name='create_address'),
    path('user/addresses/edit/<int:address_id>/', AddressUpdateView.as_view(), name='edit_address'),
    path('user/addresses/delete/<int:address_id>/', DeleteAddressView.as_view(), name='delete_address'),
    
    #City
    path('user/city/', GetCityAPIView.as_view(), name='get_city'),
    path('user/district/<int:city_id>', GetDistrictAPIView.as_view(), name='get_district'),
    path('user/neighborhood/<int:district_id>', GetNeighborhoodAPIView.as_view(), name='get_neighborhood'),

    #MyStyle
    path('user/room-type/', RoomTypeSelectionAPIView.as_view(), name='room_type_selection'),
    path('user/home-type/', HomeTypeSelectionAPIView.as_view(), name='home_type_selection'),
    path('user/home-model/', HomeModelSelectionAPIView.as_view(), name='home_model_selection'),
    path('user/space-definition/', SpaceDefinitionSelectionAPIView.as_view(), name='space_definition_selection'),
    path('user/time-range/', TimeRangeSelectionAPIView.as_view(), name='time_range_selection'),
    path('user/mystyle-List/', MyStyleListAPIView.as_view(), name='mystyle_list'),
    path('user/mystyle-category-list/', MyStyleCategoryListAPIView.as_view(), name='mystyle_category_list'),
    path('user/mystyle-category-product-list/', MyStyleCategoryProductListAPIView.as_view(), name='mystyle_category_product_list'),
    #WishList
    path('user/wishlist/', WishlistAPIView.as_view(), name='wishlist'),
    path('user/wishlist/add/<int:product_id>', AddToWishlistAPIView.as_view(), name='add_to_wishlist'),
    path('user/wishlist/remove/<int:wish_id>', RemoveFromWishlistAPIView.as_view(), name='remove_wishlist'),

    #OrderList
    path('user/orderlist/', OrderListAPIView.as_view(), name='orderlist'),
    path('user/orderdetail/<str:order_number>/', OrderDetailAPIView.as_view(), name='orderdetail'),





    path('user/notifications/', NotificationSettingsAPI.as_view(), name='api_notifications'),

]



