"""SaaSAutomation URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""


# Django Imports
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from . import yasg
from django.conf.urls import handler404
from django.views.generic import TemplateView


urlpatterns = [
    # Inbuilt Endpoints
    path('admin/', admin.site.urls),
    path('', include('apps.base_page.urls')),
    path('mainapp/', include('apps.mainapp.urls')),
    path('plans/', include('apps.plans.urls')),
    path('recruitment/', include('apps.recruitment.urls')),
    path('statistics/', include('apps.statistics.urls')),
    path('students/', include('apps.students.urls')),
    path('users/', include('apps.users.urls')),

    # API Endpoints
    path('api/users/', include('apps.users.urls_api')),
    path('api/auth_lms/', include('apps.auth_lms.urls')),
    path('api/v1/students/', include('apps.students.urls_api')),
    path('api/v1/mainapp/', include('apps.mainapp.urls_api')),
    path('api/v1/branches/', include('apps.branches.urls_api')),
    path('api/v2/sales/', include('apps.sales.urls_api')),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


# Swagger Documentation is disabled for now
urlpatterns += yasg.urlpatterns

handler404 = 'django.views.defaults.page_not_found'  # Убедитесь, что это настроено


