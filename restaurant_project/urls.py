from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from .views import home
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('usuarios/', include('usuarios.urls')),
    path('inventario/', include('inventario.urls')),
    path('app/', include('pedidos.urls')),
    path('mesas/', include('mesas.urls')),
    path('platos/', include('platos.urls')),
    path('pagos/', include('pagos.urls')),
    path('arqueo/', include('arqueo.urls')),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='registration/logged_out.html'), name='logout'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)