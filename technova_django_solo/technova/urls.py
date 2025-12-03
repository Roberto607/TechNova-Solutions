from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('newsletter/', include('newsletter.urls')),
    path('products', include('products.urls')),
    path('usuarios/', include('users.urls')),
    path('carrito/', include('orders.urls')),
    path('admin-panel/', include('admin_panel.urls')),
    
    # Páginas estáticas
    path('nosotros/', TemplateView.as_view(template_name='pages/about.html'), name='about'),
    path('terminos/', TemplateView.as_view(template_name='pages/terms.html'), name='terms'),
    path('privacidad/', TemplateView.as_view(template_name='pages/privacy.html'), name='privacy'),
    # newsletter already included above; duplicated include removed to avoid namespace warning
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
