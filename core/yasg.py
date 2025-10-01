# Auto Documentation
from django.urls import path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
# Rest Framework
from rest_framework import permissions

# Setup for Swagger Documentation
schema_view = get_schema_view(
    openapi.Info(
        title="ITC service API",
        default_version='v1',
        description="В данной документации подробно описаны все действующие API ендпоинты",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='documentation'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='redoc-documentation'),
]
