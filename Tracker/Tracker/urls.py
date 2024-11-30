from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from .views import home_view

from rest_framework.authtoken.views import obtain_auth_token
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

# Swagger/OpenAPI için yapılandırma
schema_view = get_schema_view(
    openapi.Info(
        title="Tracker API",
        default_version="v1",
        description="Tracker uygulaması için API dokümantasyonu",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="support@tracker.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_view, name='home'),
    path("accounts/", include("accounts.urls")),
    path('attendance/', include('attendance.urls')),
    path('leave/', include('leave.urls')),
    path('notifications/', include('notifications.urls')),
    path('reports/', include('reports.urls')),


    # Swagger/OpenAPI URL'leri
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
