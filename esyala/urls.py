from django.contrib import admin
from django.urls import path,include
from django.conf.urls.static import static
from esyala.settings import *

from esyala.views import CustomSpectacularAPIView, CustomSpectacularSwaggerView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("blog/", include("blog.urls")), 
    path("main/", include("main.urls")),
    path("products/", include("products.urls")),
    path("notification/", include("notification.urls")),
    path("customerauth/", include("customerauth.urls")),

    path('api/schema/', CustomSpectacularAPIView.as_view(), name='schema'),

    # Redoc ve Swagger endpointleri
    path('api/schema/swagger-ui/', CustomSpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
]


urlpatterns += static(STATIC_URL, document_root=STATIC_ROOT)
urlpatterns += static(MEDIA_URL, document_root=MEDIA_ROOT)