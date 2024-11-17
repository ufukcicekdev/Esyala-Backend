from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from django.shortcuts import redirect
from django.urls import reverse
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy


def superuser_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect(reverse('admin_login'))  # Giriş sayfasına yönlendir
        if not request.user.is_superuser:
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




class CustomLoginView(LoginView):
    template_name = 'registration/login.html'  
