from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

def superuser_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_superuser:
            from django.http import HttpResponseForbidden
            return HttpResponseForbidden("Bu sayfaya erişim yetkiniz yok.")
        return view_func(request, *args, **kwargs)
    return wrapper

@method_decorator(superuser_required, name='dispatch')
class CustomSpectacularSwaggerView(SpectacularSwaggerView):
    pass

@method_decorator(superuser_required, name='dispatch')
class CustomSpectacularAPIView(SpectacularAPIView):
    pass
